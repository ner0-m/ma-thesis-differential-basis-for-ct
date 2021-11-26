PYTHON := $(shell which python)

FIGURE_DIR := $(abspath ./figures)
PYTHON_DIR := $(abspath ./python)

.PHONY: figures

gen-figures:
	$(PYTHON) -m pylib --figure-path $(FIGURE_DIR)

distclean:
	rm -f $(FIGURE_DIR)/*.png
