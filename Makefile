SRCDIR=./ccquery
DOCDIR=./docs
PY=python3
PIP=pip3

all: check test

check: check-syntax check-lint check-dist

check-syntax:
	$(PY) -m compileall .

check-lint:
	if [ -d $(SRCDIR) ]; then $(PY) -m pylint --rcfile=.pylintrc $(SRCDIR); fi

check-dist:
	$(PY) setup.py check


test: test-unit

test-unit:
	$(PY) -m unittest discover -v

test-coverage:
	coverage run --source=$(SRCDIR) -m unittest discover
	coverage report --include='$(SRCDIR)/*' -m


docs:
	sphinx-apidoc -f -o $(DOCDIR) $(SRCDIR)
	$(PY) setup.py build_sphinx --build-dir $(DOCDIR)

build:
	$(PY) setup.py build

install:
	## using pip since fastText is not compatible with EasyInstall ...
	# $(PY) setup.py install
	$(PIP) install --process-dependency-links ".[api]"

local-install:
	$(PIP) install -r requirements.txt --process-dependency-links

clean:
	py3clean .
	$(PY) setup.py clean --all
	find . -name '*.eggs' -type d -prune -exec rm -r {} \;
	find . -name '*.egg' -type d -prune -exec rm -r {} \;
	find . -name '*.egg-info' -type d -prune -exec rm -r {} \;
	find . -name '__pycache__' -type d -prune -exec rm -r {} \;
	find . -name '*.cache' -type d -prune -exec rm -r {} \;
	find . -name '*.py[co]' -type f -exec rm {} \;
	find . -name '*.log' -type f -exec rm {} \;
	find . -name '*.egg' -type f -exec rm {} \;
	find . -name '*.coverage' -type f -exec rm {} \;
	find . -name '*.tar.xz' -type f -exec rm {} \;
	rm -rf ./build \;
	rm -rf ./dist \;
	rm -rf ./eggs \;
	rm -rf ./_rst \;
	rm -rf $(DOCDIR) \;
