""" Custom Ansible Lookup Plugin for reading dotenv files.

Ansible officially supports Python 2.7 and 3.5+, but this requires Python 3.8+.

"""
from __future__ import annotations

from typing import Sequence

from ansible.errors import AnsibleFileNotFound, AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from re import compile


__all__ = "DOCUMENTATION", "EXAMPLES", "RETURN", "LookupModule"


# Options not documented will be ignored during processing.

DOCUMENTATION = """
  name: dotenv
  author:
    - Michael Klatt <mdklatt(at)alumni.ou.edu>
  short_description: Retrieve values from dotenv files
  requirements:
    - Anisble must be running under Python 3.8+.
  description:
    - Retrieve values from dotenv values.
  seealso:
    - name: RFC 2 - .env file
      description: Smartmob RFC for a .env file standard
      link: https://smartmob-rfc.readthedocs.io/en/latest/2-dotenv.html
  notes:
    - The RFC 2 continuation line syntax is not yet supported.
  options:
    _terms:
      description: The key(s) to look up.
      required: True
    file:
      description: Path to the dotenv file.
      default: '.env'
"""  # YAML


RETURN = """
  _raw:
    description:
      - value(s) of the search term(s) in the dotenv file
    type: list
    elements: str
"""  # YAML


EXAMPLES = """
  - name: Retrieve value from the .env file in the current working directory.
    debug:
      msg: "{{ lookup('dotenv', 'VAR') }}"
  - name: Use a non-default dotenv file.
    debug:
      msg: "{{ lookup('dotenv', 'VAR', file='path/to/.env') }}"
"""  # YAML


class LookupModule(LookupBase):  # class name is not arbitrary, DO NOT CHANGE
    """ Look up values from a dotenv file.

    """
    def run(self, terms: Sequence[str], variables=None, **options) -> list:
        """ Execute the lookup.

        :param terms: search terms
        :param variables: mapping of defined Ansible variables
        :param options: options passed directly as keyword arguments
        :return: list of found values
        """
        # Adapted from 'ansible.builtin.ini' lookup.
        # <https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/ini.py>
        # <https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#developing-lookup-plugins>
        self.set_options(var_options=variables, direct=options)
        params = self.get_options()
        path = self.find_file_in_search_path(variables, "files", params["file"])
        if not path:
            raise AnsibleFileNotFound(f"Could not find file {params['file']}")
        var_pattern = compile(r"^\s*([a-zA-Z_]+[a-zA-Z0-9_]*)\s*=\s*(\S*)")
        variables = {}
        for line in open(path, "rt").readlines():
            # Parse the dotenv file permissively, accepting valid NAME=VALUE
            # lines while ignoring everything else.
            # TODO: Support RFC 2 line continuation syntax.
            if match := var_pattern.match(line):
                variables[match.group(1)] = match.group(2)
        try:
            return [variables[key] for key in terms]
        except KeyError as err:
            key = err.args[0]
            raise AnsibleLookupError(f"No value for '{key}' in {path}")
