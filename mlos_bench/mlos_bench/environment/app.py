"""
Application-specific benchmark environment.
"""

import logging
import subprocess
import sys
import tempfile
from typing import Optional

import pandas as pd

from mlos_bench.environment.status import Status
from mlos_bench.environment.base_environment import Environment
from mlos_bench.environment.base_service import Service
from mlos_bench.environment.tunable import TunableGroups

_LOG = logging.getLogger(__name__)


class AppEnv(Environment):
    """
    Application-level benchmark environment.
    """

    def __init__(self,
                 name: str,
                 config: dict,
                 global_config: Optional[dict] = None,
                 tunables: Optional[TunableGroups] = None,
                 service: Optional[Service] = None):
        # pylint: disable=too-many-arguments
        """
        Create a new application environment with a given config.

        Parameters
        ----------
        name: str
            Human-readable name of the environment.
        config : dict
            Free-format dictionary that contains the benchmark environment
            configuration. Each config must have at least the "tunable_params"
            and the "const_args" sections.
        global_config : dict
            Free-format dictionary of global parameters (e.g., security credentials)
            to be mixed in into the "const_args" section of the local config.
        tunables : TunableGroups
            A collection of tunable parameters for *all* environments.
        service: Service
            An optional service object (e.g., providing methods to
            deploy or reboot a VM, etc.).
        """
        super().__init__(name, config, global_config, tunables, service)
        self._script_setup = self.config.get("setup")
        self._script_run = self.config.get("run")
        self._script_teardown = self.config.get("teardown")
        self._script_postprocess = self.config.get("postprocess")
        if self._script_postprocess is not None:
            self._script_postprocess = self._service.resolve_path(self._script_postprocess)

    def setup(self, tunables: TunableGroups) -> bool:
        """
        Check if the environment is ready and set up the application
        and benchmarks, if necessary.

        Parameters
        ----------
        tunables : TunableGroups
            A collection of tunable OS and application parameters along with their
            values. Setting these parameters should not require an OS reboot.

        Returns
        -------
        is_success : bool
            True if operation is successful, false otherwise.
        """
        if not super().setup(tunables):
            return False

        if not self._script_setup:
            self._is_ready = True
            return True

        _LOG.info("Set up: %s", self)
        (status, _) = self._remote_exec(self._script_setup)
        _LOG.info("Set up complete: %s :: %s", self, status)
        self._is_ready = (status == Status.SUCCEEDED)
        return self._is_ready

    def teardown(self):
        """
        Clean up and shut down the application environment.
        """
        if self._script_teardown:
            _LOG.info("Tear down: %s", self)
            (status, _) = self._remote_exec(self._script_teardown)
            _LOG.info("Tear down complete: %s :: %s", self, status)
        super().teardown()

    def benchmark(self):
        """
        Submit a new experiment to the application environment.
        (Re)configure an application and launch the benchmark.

        Returns
        -------
        (benchmark_status, benchmark_result) : (enum, float)
            A pair of (benchmark status, benchmark result) values.
            benchmark_status is of type mlos_bench.environment.Status.
            benchmark_result is a floating point time of the benchmark in
            seconds or None if the status is not COMPLETED.
        """
        _LOG.info("Run benchmark on: %s", self)
        (status, _) = result = super().benchmark()
        if not (status == Status.READY and self._script_run):
            return result

        # Configure the application and start the benchmark
        (status, _) = result = self._remote_exec(self._script_run)

        if not self._script_postprocess:
            return result

        with tempfile.TemporaryDirectory() as local_dir:
            self._service.download(self._const_args["outputPrefix"], local_dir)

            # Post-process results
            proc = subprocess.run(
                [
                    # Execute the post-processing script with the current python env
                    sys.executable,
                    self._script_postprocess,
                    # Pass the download dir as the argument to the script
                    local_dir,
                ],
                shell=True,
                check=True,
                capture_output=True,
            )
            script_results = proc.stdout.decode().strip()
            if proc.returncode == 0:
                metrics_df = pd.read_csv(script_results)
            else:
                metrics_df = None
                _LOG.error(
                    "Non-zero exit code %d during post-processing with %s. STDOUT: \n%s",
                    proc.returncode, self._script_postprocess, script_results)

        result = (status, metrics_df)
        _LOG.info("Run complete: %s :: %s", self, result)
        return result

    def _remote_exec(self, script):
        """
        Run a script on the remote host.

        Parameters
        ----------
        script : [str]
            List of commands to be executed on the remote host.

        Returns
        -------
        result : (Status, dict)
            A pair of Status and result.
            Status is one of {PENDING, SUCCEEDED, FAILED, TIMED_OUT}
        """
        _LOG.debug("Submit script: %s", self)
        (status, output) = self._service.remote_exec(script, self._params)
        _LOG.debug("Script submitted: %s %s :: %s", self, status, output)
        if status in {Status.PENDING, Status.SUCCEEDED}:
            (status, output) = self._service.get_remote_exec_results(output)
            # TODO: extract the results from `output`.
        _LOG.debug("Status: %s :: %s", status, output)
        return (status, output)
