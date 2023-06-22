SRC_DIR := src
TESTS_DIR := tests

.PHONY: mypy
mypy:
	mypy $(SRC_DIR) $(TESTS_DIR)

.PHONY: pylint
pylint:
	pylint $(SRC_DIR) $(TESTS_DIR)

.PHONY: black
black:
	black $(SRC_DIR) $(TESTS_DIR)

.PHONY: lint
lint: mypy pylint black

.PHONY: test
test:
	pytest $(TESTS_DIR)
