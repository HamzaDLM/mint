# Makefile for the Mint interpreter project

# Vars
PACKAGE_NAME = mint
SRC_DIR = src
TEST_DIR = ${SRC_DIR}/tests
VENV_DIR = .venv
PYTHON = ${VENV_DIR}/bin/python
PIP = ${VENV_DIR}/bin/pip

# Default
.PHONY: all
all: install test

# Create Venv
.PHONY: venv
venv:
	python3 -m venv $(VENV_DIR)

# Install deps
.PHONY: install
install: venv
	. $(VENV_DIR)/bin/activate
	$(PIP) install -e .
	$(PIP) install -r requirements-dev.txt
	
# Run tests
.PHONY: test
test: install
	$(PYTHON) -m pytest $(TEST_DIR) 

# Run linting (Ruff)
.PHONY: lint
lint: install
	$(PYTHON) -m ruff check $(SRC_DIR) # $(TEST_DIR)

# Run formatter (Ruff)
.PHONY: format
format: install
	$(PYTHON) -m ruff format $(SRC_DIR) # $(TEST_DIR)

# Run mypy
.PHONY: mypy
mypy: install
	$(PYTHON) -m mypy $(SRC_DIR) # $(TEST_DIR)

# Run mint against a test file
.PHONY: run
run: install
	# echo $(PYTHON) mint ${TEST_DIR}/$(file)
	$(PYTHON) ${SRC_DIR}/mint.py ${TEST_DIR}/$(file)

# Clean generated files
.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache

# Display help
.PHONY: help
help:
	@echo "Makefile targets:"
	@echo "  all        - Install dependencies and run tests"
	@echo "  venv       - Create virtual environment"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  clean      - Clean generated files"
	@echo "  run        - Run the interpreter with a specified file (usage: make run file=<filename>)"
	@echo "  help       - Display this help message"
