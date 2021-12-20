.PHONY: clean all watch

all:
	latexmk -pdf -xelatex -interaction=nonstopmode main.tex
	 
watch:
	latexmk -pvc -interaction=nonstopmode

clean:
	latexmk -c
