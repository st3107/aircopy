#! /bin/bash

coverage run -m pytest # Run the tests and check for test coverage.
coverage report -m     # Generate test coverage report.
codecov                # Upload the report to codecov.
flake8                 # Enforce code style ('relaxed' line length limit is set in .flake8 config file).
make -C docs html      # Build the documentation.
if [ "$TRAVIS_BRANCH" == 'master' ] && [ "$TRAVIS_PULL_REQUEST" == 'false' ]; then # if change on master and not PR
  set -e
  pip install doctr
  doctr deploy . --built-docs docs/build/html
fi