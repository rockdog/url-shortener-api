VIRTUALENV_RUN_TARGET = virtualenv_run
VIRTUALENV_RUN_REQUIREMENTS = requirements.txt requirements-dev.txt

.PHONY: all
all: development

.PHONY: development
development: virtualenv_run install-hooks

.PHONY: test
test: clean-cache
	tox

.PHONY: install-hooks
install-hooks: virtualenv_run
	./virtualenv_run/bin/pre-commit install -f --install-hooks

.PHONY: run-hooks
run-hooks: virtualenv_run
	./virtualenv_run/bin/pre-commit run --all-files

virtualenv_run: $(VIRTUALENV_RUN_REQUIREMENTS)
	tox -e $(VIRTUALENV_RUN_TARGET)

.PHONY:
clean: clean-cache
	-rm -rf virtualenv_run/
	-rm -rf .tox

.PHONY:
clean-cache:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache
	rm -rf .pytest_cache

.PHONY:
upgrade-requirements:
	upgrade-requirements --python python3.8
