# Project management tasks.

VENV = .venv
PYTHON = . $(VENV)/bin/activate && python

export ANSIBLE_LOOKUP_PLUGINS = src:$${ANSIBLE_LOOKUP_PLUGINS}


$(VENV)/.make-update: requirements-dev.txt
	python -m venv $(VENV)
	$(PYTHON) -m pip install -U pip && for req in $^; do pip install -r "$$req"; done
	touch $@


.PHONY: dev
dev: $(VENV)/.make-update


.PHONY: test
test:
	$(PYTHON) -m pytest tests/
