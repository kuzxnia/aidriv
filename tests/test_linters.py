from __future__ import print_function

from subprocess import CalledProcessError, check_output

FLAKE8_COMMAND = "flake8"
PYLINT_COMMAND = "pylint"
LINTER_INPUTS = ["aidriv", "tests"]


def pytest_generate_tests(metafunc):
    metafunc.parametrize("directory", LINTER_INPUTS)


def test_flake8(directory):
    _test_linter(FLAKE8_COMMAND, directory)


def test_pylint(directory):
    _test_linter(PYLINT_COMMAND, directory)


def _test_linter(command, path):
    try:
        check_output([command, path])
    except CalledProcessError as e:
        raise AssertionError(
            f"{command} has found errors.\n\n {e.output.decode('utf8')}"
        )
    except OSError:
        raise OSError(
            f"Failed to run {command}. Please check that you have installed it properly."
        )
