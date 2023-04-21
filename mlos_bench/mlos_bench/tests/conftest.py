#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
#
"""
Common fixtures for mock TunableGroups and Environment objects.
"""

import pytest

from mlos_bench.environment.mock_env import MockEnv
from mlos_bench.tunables.tunable_groups import TunableGroups

# pylint: disable=redefined-outer-name
# -- Ignore pylint complaints about pytest references to
# `tunable_groups` fixture as both a function and a parameter.


@pytest.fixture
def tunable_groups() -> TunableGroups:
    """
    A test fixture that produces a mock TunableGroups.

    Returns
    -------
    tunable_groups : TunableGroups
        A new TunableGroups object for testing.
    """
    tunables = TunableGroups({
        "provision": {
            "cost": 1000,
            "params": {
                "vmSize": {
                    "description": "Azure VM size",
                    "type": "categorical",
                    "default": "Standard_B4ms",
                    "values": ["Standard_B2s", "Standard_B2ms", "Standard_B4ms"]
                }
            }
        },
        "boot": {
            "cost": 300,
            "params": {
                "rootfs": {
                    "description": "Root file system",
                    "type": "categorical",
                    "default": "xfs",
                    "values": ["xfs", "ext4", "ext2"]
                }
            }
        },
        "kernel": {
            "cost": 1,
            "params": {
                "kernel_sched_migration_cost_ns": {
                    "description": "Cost of migrating the thread to another core",
                    "type": "int",
                    "default": -1,
                    "range": [-1, 500000],
                    "special": [-1]
                },
                "kernel_sched_latency_ns": {
                    "description": "Initial value for the scheduler period",
                    "type": "int",
                    "default": 2000000,
                    "range": [0, 1000000000]
                }
            }
        }
    })
    tunables.reset()
    return tunables


@pytest.fixture
def mock_env(tunable_groups: TunableGroups) -> MockEnv:
    """
    Test fixture for MockEnv.
    """
    return MockEnv(
        name="Test Env",
        config={
            "tunable_groups": ["provision", "boot", "kernel"],
            "seed": 13,
            "range": [60, 120]
        },
        tunables=tunable_groups
    )


@pytest.fixture
def mock_env_no_noise(tunable_groups: TunableGroups) -> MockEnv:
    """
    Test fixture for MockEnv.
    """
    return MockEnv(
        name="Test Env No Noise",
        config={
            "tunable_groups": ["provision", "boot", "kernel"],
            "range": [60, 120]
        },
        tunables=tunable_groups
    )