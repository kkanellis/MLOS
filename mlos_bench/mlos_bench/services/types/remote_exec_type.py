#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
"""
Protocol interface for Service types that provide helper functions to run
scripts on a remote host OS.
"""

from typing import Iterable, Tuple, Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from mlos_bench.environments.status import Status


@runtime_checkable
class SupportsRemoteExec(Protocol):
    """
    Protocol interface for Service types that provide helper functions to run
    scripts on a remote host OS.
    """

    def remote_exec(self, script: Iterable[str], params: dict) -> Tuple["Status", dict]:
        """
        Run a command on remote host OS.

        Parameters
        ----------
        script : Iterable[str]
            A list of lines to execute as a script on a remote VM.
        params : dict
            Flat dictionary of (key, value) pairs of parameters.
            They usually come from `const_args` and `tunable_params`
            properties of the Environment.

        Returns
        -------
        result : (Status, dict)
            A pair of Status and result.
            Status is one of {PENDING, SUCCEEDED, FAILED}
        """

    def get_remote_exec_results(self, params: dict) -> Tuple["Status", dict]:
        """
        Get the results of the asynchronously running command.

        Parameters
        ----------
        params : dict
            Flat dictionary of (key, value) pairs of tunable parameters.
            Must have the "asyncResultsUrl" key to get the results.
            If the key is not present, return Status.PENDING.

        Returns
        -------
        result : (Status, dict)
            A pair of Status and result.
            Status is one of {PENDING, SUCCEEDED, FAILED, TIMED_OUT}
        """
