#####################
ansible-dotenv-lookup
#####################

|python|
|license|
|tests|

This is an `Ansible lookup plugin`_ for retrieving values from a dotenv file
that conforms to `Smartmob RFC 2`_, although continuation lines are not yet
supported.


============
Requirements
============

- Python 3.8+ is required for the Ansible control node.


============
Installation
============

The plugin source file must be visible in one of these locations (see
`enabling lookup plugins`_):

- The ``lookup_plugins/`` directory adjacent to the play
- The ``plugins/lookup/`` directory of a collection or role
- The value of the `DEFAULT_LOOKUP_PLUGIN_PATH`_ config variable


===========
Development
===========

A local virtualenv using the minimum supported Python version (currently
``3.8``) is recommend for development. The included *Makefile* automates
project tasks:

.. code-block:: console

    $ pyenv local 3.8.13
    $ make dev
    $ make test


.. |python| image:: https://img.shields.io/static/v1?label=python&message=3.8%2B&color=informational
    :alt: Python 3.8+
.. |license| image:: https://img.shields.io/github/license/mdklatt/ansible-dotenv-lookup
    :alt: MIT License
    :target: `MIT License`_
.. |tests| image:: https://github.com/mdklatt/ansible-dotenv-lookup/actions/workflows/tests.yml/badge.svg
    :alt: CI Tests
    :target: `GitHub Actions`_

.. _MIT License: https://choosealicense.com/licenses/mit
.. _GitHub Actions: https://github.com/mdklatt/ansible-dotenv-lookup/actions/workflows/tests.yml
.. _Ansible lookup plugin: https://docs.ansible.com/ansible/latest/plugins/lookup.html
.. _Smartmob RFC 2: https://smartmob-rfc.readthedocs.io/en/latest/2-dotenv.html
.. _enabling lookup plugins: https://docs.ansible.com/ansible/latest/plugins/lookup.html#enabling-lookup-plugins
.. _DEFAULT_LOOKUP_PLUGIN_PATH: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#default-lookup-plugin-path