#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
"""
Local Environments for mlos_bench.
"""

from mlos_bench.environments.local.local_env import LocalEnv
from mlos_bench.environments.local.local_env_fileshare import LocalFileShareEnv

__all__ = [
    'LocalEnv',
    'LocalFileShareEnv',
]
