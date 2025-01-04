#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
"""
DB schema definition for the :py:class:`~mlos_bench.storage.sql.storage.SqlStorage`
backend.

Notes
-----
The SQL statements are generated by SQLAlchemy, but can be obtained using
``repr`` or ``str`` (e.g., via ``print()``) on this object.
The ``mlos_bench`` CLI will do this automatically if the logging level is set to
``DEBUG``.

Also see the `mlos_bench CLI usage <../../../../../mlos_bench.run.usage.html>`__ for
details on how to invoke only the schema creation/update routines.
"""

import logging
from importlib.resources import files
from typing import Any

from alembic import command, config
from sqlalchemy import (
    Column,
    DateTime,
    Dialect,
    Float,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    Sequence,
    String,
    Table,
    UniqueConstraint,
    create_mock_engine,
)
from sqlalchemy.engine import Engine

from mlos_bench.util import path_join

_LOG = logging.getLogger(__name__)


class _DDL:
    """
    A helper class to capture the DDL statements from SQLAlchemy.

    It is used in `DbSchema.__str__()` method below.
    """

    def __init__(self, dialect: Dialect):
        self._dialect = dialect
        self.statements: list[str] = []

    def __call__(self, sql: Any, *_args: Any, **_kwargs: Any) -> None:
        self.statements.append(str(sql.compile(dialect=self._dialect)))

    def __repr__(self) -> str:
        res = ";\n".join(self.statements)
        return res + ";" if res else ""


class DbSchema:
    """A class to define and create the DB schema."""

    # This class is internal to SqlStorage and is mostly a struct
    # for all DB tables, so it's ok to disable the warnings.
    # pylint: disable=too-many-instance-attributes

    # Common string column sizes.
    _ID_LEN = 512
    _PARAM_VALUE_LEN = 1024
    _METRIC_VALUE_LEN = 255
    _STATUS_LEN = 16

    def __init__(self, engine: Engine | None):
        """
        Declare the SQLAlchemy schema for the database.

        Parameters
        ----------
        engine : sqlalchemy.engine.Engine | None
            The SQLAlchemy engine to use for the DB schema.
            Listed as optional for `alembic <https://alembic.sqlalchemy.org>`_
            schema migration purposes so we can reference it inside it's ``env.py``
            config file for :attr:`~meta` data inspection, but won't generally be
            functional without one.
        """
        _LOG.info("Create the DB schema for: %s", engine)
        self._engine = engine
        self._meta = MetaData()

        self.experiment = Table(
            "experiment",
            self._meta,
            Column("exp_id", String(self._ID_LEN), nullable=False),
            Column("description", String(1024)),
            Column("root_env_config", String(1024), nullable=False),
            Column("git_repo", String(1024), nullable=False),
            Column("git_commit", String(40), nullable=False),
            PrimaryKeyConstraint("exp_id"),
        )
        """The Table storing
        :py:class:`~mlos_bench.storage.base_experiment_data.ExperimentData` info.
        """

        self.objectives = Table(
            "objectives",
            self._meta,
            Column("exp_id"),
            Column("optimization_target", String(self._ID_LEN), nullable=False),
            Column("optimization_direction", String(4), nullable=False),
            # TODO: Note: weight is not fully supported yet as currently
            # multi-objective is expected to explore each objective equally.
            # Will need to adjust the insert and return values to support this
            # eventually.
            Column("weight", Float, nullable=True),
            PrimaryKeyConstraint("exp_id", "optimization_target"),
            ForeignKeyConstraint(["exp_id"], [self.experiment.c.exp_id]),
        )
        """The Table storing
        :py:class:`~mlos_bench.storage.base_storage.Storage.Experiment` optimization
        objectives info.
        """

        # A workaround for SQLAlchemy issue with autoincrement in DuckDB:
        if engine and engine.dialect.name == "duckdb":
            seq_config_id = Sequence("seq_config_id")
            col_config_id = Column(
                "config_id",
                Integer,
                seq_config_id,
                server_default=seq_config_id.next_value(),
                nullable=False,
                primary_key=True,
            )
        else:
            col_config_id = Column(
                "config_id",
                Integer,
                nullable=False,
                primary_key=True,
                autoincrement=True,
            )

        self.config = Table(
            "config",
            self._meta,
            col_config_id,
            Column("config_hash", String(64), nullable=False, unique=True),
        )
        """The Table storing
        :py:class:`~mlos_bench.storage.base_tunable_config_data.TunableConfigData`
        info.
        """

        self.trial = Table(
            "trial",
            self._meta,
            Column("exp_id", String(self._ID_LEN), nullable=False),
            Column("trial_id", Integer, nullable=False),
            Column("config_id", Integer, nullable=False),
            Column("ts_start", DateTime, nullable=False),
            Column("ts_end", DateTime),
            # Should match the text IDs of `mlos_bench.environments.Status` enum:
            Column("status", String(self._STATUS_LEN), nullable=False),
            PrimaryKeyConstraint("exp_id", "trial_id"),
            ForeignKeyConstraint(["exp_id"], [self.experiment.c.exp_id]),
            ForeignKeyConstraint(["config_id"], [self.config.c.config_id]),
        )
        """The Table storing :py:class:`~mlos_bench.storage.base_trial_data.TrialData`
        info.
        """

        # Values of the tunable parameters of the experiment,
        # fixed for a particular trial config.
        self.config_param = Table(
            "config_param",
            self._meta,
            Column("config_id", Integer, nullable=False),
            Column("param_id", String(self._ID_LEN), nullable=False),
            Column("param_value", String(self._PARAM_VALUE_LEN)),
            PrimaryKeyConstraint("config_id", "param_id"),
            ForeignKeyConstraint(["config_id"], [self.config.c.config_id]),
        )
        """The Table storing
        :py:class:`~mlos_bench.storage.base_tunable_config_data.TunableConfigData`
        info.
        """

        # Values of additional non-tunable parameters of the trial,
        # e.g., scheduled execution time, VM name / location, number of repeats, etc.
        self.trial_param = Table(
            "trial_param",
            self._meta,
            Column("exp_id", String(self._ID_LEN), nullable=False),
            Column("trial_id", Integer, nullable=False),
            Column("param_id", String(self._ID_LEN), nullable=False),
            Column("param_value", String(self._PARAM_VALUE_LEN)),
            PrimaryKeyConstraint("exp_id", "trial_id", "param_id"),
            ForeignKeyConstraint(
                ["exp_id", "trial_id"],
                [self.trial.c.exp_id, self.trial.c.trial_id],
            ),
        )
        """The Table storing :py:class:`~mlos_bench.storage.base_trial_data.TrialData`
        :py:attr:`metadata <mlos_bench.storage.base_trial_data.TrialData.metadata_dict>`
        info.
        """

        self.trial_status = Table(
            "trial_status",
            self._meta,
            Column("exp_id", String(self._ID_LEN), nullable=False),
            Column("trial_id", Integer, nullable=False),
            Column("ts", DateTime(timezone=True), nullable=False, default="now"),
            Column("status", String(self._STATUS_LEN), nullable=False),
            UniqueConstraint("exp_id", "trial_id", "ts"),
            ForeignKeyConstraint(
                ["exp_id", "trial_id"],
                [self.trial.c.exp_id, self.trial.c.trial_id],
            ),
        )
        """The Table storing :py:class:`~mlos_bench.storage.base_trial_data.TrialData`
        :py:class:`~mlos_bench.environments.status.Status` info.
        """

        self.trial_result = Table(
            "trial_result",
            self._meta,
            Column("exp_id", String(self._ID_LEN), nullable=False),
            Column("trial_id", Integer, nullable=False),
            Column("metric_id", String(self._ID_LEN), nullable=False),
            Column("metric_value", String(self._METRIC_VALUE_LEN)),
            PrimaryKeyConstraint("exp_id", "trial_id", "metric_id"),
            ForeignKeyConstraint(
                ["exp_id", "trial_id"],
                [self.trial.c.exp_id, self.trial.c.trial_id],
            ),
        )
        """The Table storing :py:class:`~mlos_bench.storage.base_trial_data.TrialData`
        :py:attr:`results <mlos_bench.storage.base_trial_data.TrialData.results_dict>`
        info.
        """

        self.trial_telemetry = Table(
            "trial_telemetry",
            self._meta,
            Column("exp_id", String(self._ID_LEN), nullable=False),
            Column("trial_id", Integer, nullable=False),
            Column("ts", DateTime(timezone=True), nullable=False, default="now"),
            Column("metric_id", String(self._ID_LEN), nullable=False),
            Column("metric_value", String(self._METRIC_VALUE_LEN)),
            UniqueConstraint("exp_id", "trial_id", "ts", "metric_id"),
            ForeignKeyConstraint(
                ["exp_id", "trial_id"],
                [self.trial.c.exp_id, self.trial.c.trial_id],
            ),
        )
        """The Table storing :py:class:`~mlos_bench.storage.base_trial_data.TrialData`
        :py:attr:`telemetry <mlos_bench.storage.base_trial_data.TrialData.telemetry_df>`
        info.
        """

        _LOG.debug("Schema: %s", self._meta)

    @property
    def meta(self) -> MetaData:
        """Return the SQLAlchemy MetaData object."""
        return self._meta

    def create(self) -> "DbSchema":
        """Create the DB schema."""
        _LOG.info("Create the DB schema")
        assert self._engine
        self._meta.create_all(self._engine)
        return self

    def update(self) -> "DbSchema":
        """
        Updates the DB schema to the latest version.

        Notes
        -----
        Also see the `mlos_bench CLI usage <../../../../../mlos_bench.run.usage.html>`__
        for details on how to invoke only the schema creation/update routines.
        """
        assert self._engine
        alembic_cfg = config.Config(
            path_join(str(files("mlos_bench.storage.sql")), "alembic.ini", abs_path=True)
        )
        with self._engine.connect() as conn:
            alembic_cfg.attributes["connection"] = conn
            command.upgrade(alembic_cfg, "head")
        return self

    def __repr__(self) -> str:
        """
        Produce a string with all SQL statements required to create the schema from
        scratch in current SQL dialect.

        That is, return a collection of CREATE TABLE statements and such.
        NOTE: this method is quite heavy! We use it only once at startup
        to log the schema, and if the logging level is set to DEBUG.

        Returns
        -------
        sql : str
            A multi-line string with SQL statements to create the DB schema from scratch.
        """
        assert self._engine
        ddl = _DDL(self._engine.dialect)
        mock_engine = create_mock_engine(self._engine.url, executor=ddl)
        self._meta.create_all(mock_engine, checkfirst=False)
        return str(ddl)
