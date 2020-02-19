from __future__ import print_function

from subprocess import CalledProcessError, check_output

BLACK_COMMAND = "black"
BLACK_OPTIONS = ["--check"]
FLAKE8_COMMAND = "flake8"
PYLINT_COMMAND = "pylint"
LINTER_INPUTS = ["aidriv", "tests"]


def pytest_generate_tests(metafunc):
    metafunc.parametrize("directory", LINTER_INPUTS)


def test_flake8(directory):
    _test_linter(FLAKE8_COMMAND, directory)


def test_pylint(directory):
    _test_linter(PYLINT_COMMAND, directory)


def test_black(directory):
    _test_linter(BLACK_COMMAND, directory, BLACK_OPTIONS)


def _test_linter(command, path, options=None):
    cmd = [command, path]
    if options is not None:
        cmd += options
    try:
        check_output(cmd)
    except CalledProcessError as e:
        raise AssertionError(
            f"{command} has found errors.\n\n {e.output.decode('utf8')}"
        )
    except OSError:
        raise OSError(
            f"Failed to run {command}. Please check that you have installed it properly."
        )
