.PHONY: lint format test install

DIRS = src/ tests/

lint:
	ruff check --fix $(DIRS)

format:
	ruff format $(DIRS)

test:
	pytest

install:
	pip3 install -e .

all: lint format install
