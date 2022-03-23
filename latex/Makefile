.PHONY: clean all watch

all:
	latexmk -pdf -xelatex -interaction=nonstopmode --outdir=build main.tex
	 
watch:
	latexmk -pvc -pdf -xelatex -interaction=nonstopmode --outdir=build main.tex

clean:
	latexmk -C
