
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
		program_proofs.tex \
		abstract.tex \
		macros.tex \
		appendix/hld.tex \
		appendix/fragment.tex \
		appendix/lld.tex \
		hld/step.tex \
		lld/step.tex \
		lld/match-p.tex \
		lld/match-bang-p.tex \
		lld/der-comp.tex \
		lld/der-agg.tex \
		lld/comp-fix.tex \
		lld/comp-match-p.tex \
		lld/comp-match-bang-p.tex \
		lld/comp-cont-c.tex \
		lld/comp-der.tex \
		lld/comp-der-end.tex \
		lld/comprehensions.tex \
		lld/agg-match-p.tex \
		lld/agg-match-bang-p.tex \
		lld/agg-cont-end.tex \
		lld/agg-cont-c.tex \
		lld/agg-cont-p.tex \
		lld/agg-fix.tex \
		lld/aggregates.tex \
		lld/soundness.tex \
		lld/comprehensions_soundness.tex \
		lld/aggregates_soundness.tex \
		lld.tex hld.tex sequent_calculus.tex
	pdflatex thesis.tex
	pdflatex thesis.tex
	bibtex thesis
	pdflatex thesis.tex
	pdflatex thesis.tex

language.tex: figures/btree/btree_trace1.pdf figures/btree/btree_trace2.pdf \
	figures/btree/btree_trace3.pdf figures/btree/btree_trace4.pdf \
	figures/message/message_trace1.pdf figures/message/message_trace2.pdf \
	figures/message/message_trace3.pdf figures/message/message_trace4.pdf \
	figures/visit/trace1.pdf figures/visit/trace2.pdf \
	figures/visit/trace3.pdf figures/visit/trace4.pdf

clean:
	rm -f thesis.pdf *.bbl *.blg *.log *.lot \
		*.brf *.lof *.toc *.out \
		*.aux *.log
