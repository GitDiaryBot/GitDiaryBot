.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

BROWSER := open
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '.eggs' -type d -exec rm -rf {} +
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	tox -e lint

test: ## run all tests
	tox -p auto

coverage: ## check code coverage quickly with the default Python
	coverage run --source diarybot pytest
	
		coverage report -m
		coverage html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/diarybot.rst
	rm -f docs/modules.rst
	pydeps diarybot/ -o docs/pydeps.svg --no-show
	sphinx-apidoc -o docs/ diarybot
	$(MAKE) -C docs clean html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## package and upload a release
	python setup.py sdist bdist_wheel
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: ## install the package with dev dependencies
	pip install -e . -r requirements/local.txt

sync: ## completely sync installed packages with dev dependencies
	pip-sync requirements/local.txt
	pip install -e .

upgrade:
	tox -e upgrade

lock:
	tox -e lock
