PYTHON := $(shell which python)

FIGURE_DIR := $(abspath ./figures)
PYTHON_DIR := $(abspath ./python)

LATEX_BUILD_DIR := ./build

.PHONY: figures distclean

thesis:
	latexmk -pdf -xelatex -interaction=nonstopmode -shell-escape --outdir=$(LATEX_BUILD_DIR) main.tex
	 
watch:
	latexmk -pvc -pdf -xelatex -interaction=nonstopmode -shell-escape --outdir=$(LATEX_BUILD_DIR) main.tex

clean-latex:
	latexmk --outdir=$(LATEX_BUILD_DIR) -C

distclean:
	rm -rf $(FIGURE_DIR)/*.png build/
