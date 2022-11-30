""" Test suite for the 'dotenv' lookup plugin.

The script can be executed on its own or incorporated into a larger test suite.

"""
from os import getcwd

import pytest
from ansible.errors import AnsibleFileNotFound, AnsibleLookupError
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.loader import lookup_loader


@pytest.fixture(scope="module")
def plugin():
    """ Load the 'dotenv' lookup plugin.

    :return: plugin instance
    """
    return lookup_loader.get("dotenv", loader=DataLoader())


@pytest.fixture(scope="module")
def dotenv() -> str:
    """ Path to the test dotenv file.

    :return: dotenv path
    """
    # Assumes project root is the working directory.
    return "tests/test.env"


@pytest.fixture
def variables() -> dict:
    """ Return predefined Ansible variables for testing.

    :return: variable mapping
    """
    # Required to use LookupBase.find_file_in_search_path() in the plugin.
    return {"ansible_search_path": [getcwd()]}


def test_lookup(plugin, dotenv, variables):
    """ Test value lookup.

    """
    terms = "VAR2", "VAR1"  # test subset of dotenv file in arbitrary order
    result = plugin.run(terms, variables, file=dotenv)
    assert result == ["VALUE2", "VALUE1"]
    return


def test_lookup_no_name(plugin, dotenv, variables):
    """ Test value lookup for an nonexistent variable.

    """
    with pytest.raises(AnsibleLookupError):
        plugin.run(["VAR0"], variables, file=dotenv)
    return


def test_lookup_no_file(plugin, dotenv, variables):
    """ Test value lookup for an nonexistent variable.

    """
    with pytest.raises(AnsibleFileNotFound):
        plugin.run(["VAR1"], variables, file="none")
    return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

