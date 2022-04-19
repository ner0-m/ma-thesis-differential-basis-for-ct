PYTHON := $(shell which python)

FIGURE_DIR := $(abspath ./figures)
PYTHON_DIR := $(abspath ./python)

LATEX_BUILD_DIR := ./build

TEXTIDOTE ?= $(shell which textidote || echo .textidote-not-found)

# Change this!
ELSA_EXAMPLE_ARGPASE_PATH?=

.PHONY: thesis figures distclean figures/experiments/artifacts

.%-not-found:
	@echo "-----------------------"
	@echo "Need $(@:.%-not-found=%). Please install it "
	@echo "-----------------------"
	@exit 1


$(LATEX_BUILD_DIR)/main.pdf: main.tex
	latexmk -pdf -pv -xelatex -interaction=nonstopmode -shell-escape --outdir=$(LATEX_BUILD_DIR) main.tex

thesis: $(LATEX_BUILD_DIR)/main.pdf
	
watch:
	latexmk -pvc -pdf -xelatex -interaction=nonstopmode -shell-escape --outdir=$(LATEX_BUILD_DIR) main.tex

clean-latex:
	latexmk --outdir=$(LATEX_BUILD_DIR) -C

toc:
	pdftk $(LATEX_BUILD_DIR)/main.pdf cat 6-7 output $(LATEX_BUILD_DIR)/main_toc.pdf

check:
	$(TEXTIDOTE) --output plain --check en --dict dict.txt main.tex | tee $(LATEX_BUILD_DIR)/report.txt

check-html:
	$(TEXTIDOTE) --output html --check en --dict dict.txt main.tex > $(LATEX_BUILD_DIR)/report.html

distclean:
	rm -rf $(FIGURE_DIR)/*.png build/

word:
	pdftotext $(LATEX_BUILD_DIR)/main.pdf - | wc -w

ifdef ELSA_EXAMPLE_ARGPASE_PATH
figures/experiments/forward_projection:
	./figures/experiments/forward_projection/run.sh $(ELSA_EXAMPLE_ARGPASE_PATH)

figures/experiments/reconstruction_rectangle:
	./figures/experiments/reconstruction_rectangle/run.sh $(ELSA_EXAMPLE_ARGPASE_PATH)

figures/experiments/reconstruction_shepp_logan:
	./figures/experiments/reconstruction_shepp_logan/run.sh $(ELSA_EXAMPLE_ARGPASE_PATH)

figures/experiments/reconstruction_fewangles:
	./figures/experiments/reconstruction_fewangles/run.sh $(ELSA_EXAMPLE_ARGPASE_PATH)
else
$(info Set ELSA_EXAMPLE_ARGPASE_PATH to the path of the elsa example_argparse executable)
endif

figures: figures/*/*
