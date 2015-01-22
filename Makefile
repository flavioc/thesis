
all: thesis.pdf

thesis.pdf: thesis.tex	\
		introduction.tex \
		coordination.tex \
		implementation.tex \
		language.tex \
		experiments.tex \
		logic_foundations.tex \
		refs.bib \
		thread.tex \
		applications.tex \
		conclusions.tex \
		appendix.tex \
		statement.tex \
		related_work.tex \
		abstract.tex \
		execution_trace1.pdf execution_trace2.pdf execution_trace3.pdf execution_trace4.pdf
	pdflatex thesis.tex
	pdflatex thesis.tex
	bibtex thesis
	pdflatex thesis.tex
	pdflatex thesis.tex

clean:
	rm -f thesis.pdf *.bbl *.blg *.log *.lot \
		*.brf *.lof *.toc *.out \
		*.aux *.log
