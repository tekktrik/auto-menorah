# SPDX-FileCopyrightText: 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`conftest.py`
=============

Configuration file for pytest

# Author(s): Alec Delaney

"""

import sys
import socket
import importlib

MODULE_NAMES = ["wifi", "secrets", "pwmio"]

for name in MODULE_NAMES:

    _spec = importlib.machinery.ModuleSpec(name, None)
    _module = importlib.util.module_from_spec(_spec)
    sys.modules[name] = _module

sys.modules["socketpool"] = socket


def pytest_addoption(parser):
    """Add options for the pytest command line"""

    parser.addoption("--aio_username", action="store")
    parser.addoption("--aio_key", action="store")
    parser.addoption("--location", action="store")


def pytest_generate_tests(metafunc):
    """Generate pytest tests"""

    aio_username = metafunc.config.option.aio_username
    aio_key = metafunc.config.option.aio_key
    location = metafunc.config.option.location

    print("FDSFJNDSJFBSDJ")
    if "aio_username" in metafunc.fixturenames and aio_username is not None:
        metafunc.parametrize("aio_username", [aio_username])
    if "aio_key" in metafunc.fixturenames and aio_key is not None:
        metafunc.parametrize("aio_key", [aio_key])
    if "location" in metafunc.fixturenames and location is not None:
        metafunc.parametrize("location", [location])
