#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
"""
A wrapper for mlos_core optimizers for mlos_bench.
"""

import logging
from typing import Optional, Sequence, Tuple, Union

import pandas as pd

from mlos_core.optimizers import BaseOptimizer, OptimizerType, OptimizerFactory, SpaceAdapterType, DEFAULT_OPTIMIZER_TYPE

from mlos_bench.environments.status import Status
from mlos_bench.tunables.tunable_groups import TunableGroups

from mlos_bench.optimizers.base_optimizer import Optimizer
from mlos_bench.services.base_service import Service
from mlos_bench.optimizers.convert_configspace import tunable_groups_to_configspace

_LOG = logging.getLogger(__name__)


class MlosCoreOptimizer(Optimizer):
    """
    A wrapper class for the mlos_core optimizers.
    """

    def __init__(self, tunables: TunableGroups, service: Optional[Service], config: dict):

        super().__init__(tunables, service, config)

        space = tunable_groups_to_configspace(tunables)
        _LOG.debug("ConfigSpace: %s", space)

        opt_type = getattr(OptimizerType, self._config.pop('optimizer_type', DEFAULT_OPTIMIZER_TYPE.name))

        space_adapter_type = self._config.pop('space_adapter_type', None)
        space_adapter_config = self._config.pop('space_adapter_config', {})

        if space_adapter_type is not None:
            space_adapter_type = getattr(SpaceAdapterType, space_adapter_type)

        self._opt: BaseOptimizer = OptimizerFactory.create(
            space, opt_type, optimizer_kwargs=self._config,
            space_adapter_type=space_adapter_type,
            space_adapter_kwargs=space_adapter_config)

    def bulk_register(self, configs: Sequence[dict], scores: Sequence[Optional[float]],
                      status: Optional[Sequence[Status]] = None) -> bool:
        if not super().bulk_register(configs, scores, status):
            return False
        # By default, hyperparameters in ConfigurationSpace are sorted by name:
        tunables_names = sorted(self._tunables.get_param_values().keys())
        df_configs = pd.DataFrame(configs)[tunables_names]
        df_scores = pd.Series(scores, dtype=float) * self._opt_sign
        if status is not None:
            # TODO: mlos_core currently does not support registration of failed trials:
            df_status_ok = pd.Series(status) == Status.SUCCEEDED
            df_configs = df_configs[df_status_ok]
            df_scores = df_scores[df_status_ok]
        # External data can have incorrect types (e.g., all strings).
        for (tunable, _group) in self._tunables:
            df_configs[tunable.name] = df_configs[tunable.name].astype(tunable.dtype)
        self._opt.register(df_configs, df_scores)
        if _LOG.isEnabledFor(logging.DEBUG):
            (score, _) = self.get_best_observation()
            _LOG.debug("Warm-up end: %s = %s", self.target, score)
        return True

    def suggest(self) -> TunableGroups:
        use_defaults = self._use_defaults and self._iter == 1
        df_config = self._opt.suggest(defaults=use_defaults)
        _LOG.info("Iteration %d :: Suggest:\n%s", self._iter, df_config)
        return self._tunables.copy().assign(df_config.loc[0].to_dict())

    def register(self, tunables: TunableGroups, status: Status,
                 score: Optional[Union[float, dict]] = None) -> Optional[float]:
        score = super().register(tunables, status, score)
        # TODO: mlos_core currently does not support registration of failed trials:
        if status.is_succeeded:
            # By default, hyperparameters in ConfigurationSpace are sorted by name:
            df_config = pd.DataFrame(dict(sorted(tunables.get_param_values().items())), index=[0])
            _LOG.debug("Score: %s Dataframe:\n%s", score, df_config)
            self._opt.register(df_config, pd.Series([score], dtype=float))
        self._iter += 1
        return score

    def get_best_observation(self) -> Union[Tuple[float, TunableGroups], Tuple[None, None]]:
        df_config = self._opt.get_best_observation()
        if len(df_config) == 0:
            return (None, None)
        params = df_config.iloc[0].to_dict()
        _LOG.debug("Best observation: %s", params)
        score = params.pop("score") * self._opt_sign  # mlos_core always uses the `score` column
        return (score, self._tunables.copy().assign(params))
