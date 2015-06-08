
EXPERIMENT_FILES := experiments/absolute/runtime.tex \
	experiments/mem/mem.tex experiments/mem/c-mem.tex \
	experiments/absolute/compare.tex

FIGURES := $(wildcard figures/btree/btree_trace*.pdf) \
	$(wildcard figures/message/message_trace*.pdf) \
	$(wildcard figures/visit/trace*.pdf) \
	$(wildcard figures/sssp/coord*.pdf) \
	$(wildcard figures/sssp/shortest.pdf)

all: thesis.pdf

thesis.pdf: thesis.tex packages.tex	thesis-cover.tex ack.tex \
		introduction.tex coordination.tex language/key_value.tex \
		language/syntax.tex language/pagerank.tex language/quicksort.tex \
		language/message_routing.tex language/graph_visit.tex \
		language/applications.tex language/related_work.tex \
		implementation.tex logic/related_work.tex \
		implementation/node.tex implementation/coord.tex \
		implementation/overview.tex implementation/comp.tex \
		implementation/parallelism.tex implementation/locks.tex \
		implementation/related_work.tex implementation/evaluation.tex \
		coordination/partitioning.tex coordination/scheduling.tex \
		coordination/ht.tex language/bipartite.tex \
		coordination/types.tex coordination/rationale.tex \
		coordination/coord_sssp.tex coordination/programs.tex \
		coordination/minimax.tex coordination/queens.tex \
		coordination/bp.tex coordination/related_work.tex \
		language.tex logic_foundations.tex threads/summary.tex \
		threads/related_work.tex background/parallel_programming.tex \
		background/declarative.tex background/provability.tex \
		refs.bib thread.tex conclusions.tex \
		appendix.tex appendix/vm.tex threads/modeling.tex \
		statement.tex abstract.tex background.tex \
		threads/graph_reachability.tex threads/implementation.tex \
		threads/key_value.tex implementation/allocation.tex \
		threads/powergrid.tex threads/splash-bp.tex \
		macros.tex appendix/hld.tex appendix/further_examples.tex \
		appendix/fragment.tex appendix/lld.tex appendix/pagerank.tex \
		hld/step.tex hld/derivation-agg.tex lld/step.tex lld/match-p.tex \
		lld/match-bang-p.tex lld/der-comp.tex \
		lld/der-agg.tex lld/comp-fix.tex \
		lld/comp-match-p.tex lld/comp-match-bang-p.tex \
		lld/comp-cont-c.tex lld/comp-der.tex \
		lld/comp-der-end.tex lld/comprehensions.tex \
		lld/agg-match-p.tex lld/agg-match-bang-p.tex lld/agg-match-other.tex \
		lld/agg-match-soundness.tex lld/agg-cont-end.tex \
		lld/agg-cont-c.tex lld/agg-cont-p.tex lld/agg-fix.tex lld/agg-der.tex \
		lld/cont-p.tex lld/cont-bang-p.tex lld/der-p.tex lld/der-other.tex \
		lld/aggregates.tex lld/soundness.tex \
		lld/comprehensions_soundness.tex lld/aggregates_soundness.tex \
		lld.tex hld.tex sequent_calculus.tex \
		$(EXPERIMENT_FILES) \
		$(FIGURES)
	latexmk -pdf thesis.tex

language.tex: figures/btree/btree_trace1.pdf figures/btree/btree_trace2.pdf \
	figures/btree/btree_trace3.pdf figures/btree/btree_trace4.pdf \
	figures/message/message_trace1.pdf figures/message/message_trace2.pdf \
	figures/message/message_trace3.pdf figures/message/message_trace4.pdf \
	figures/visit/trace1.pdf figures/visit/trace2.pdf \
	figures/visit/trace3.pdf figures/visit/trace4.pdf

RE := PYTHONPATH=$(PWD)/experiments:$(PYTHONPATH) python

experiments/absolute/runtime.tex: experiments/lib.py experiments/absolute/table.py \
	experiments/absolute/runtime.csv
	$(RE) experiments/absolute/table.py \
				  experiments/absolute/runtime.csv > experiments/absolute/runtime.tex

experiments/mem/mem.tex: experiments/lib.py experiments/mem/table.py \
	experiments/mem/mem.csv
	$(RE) experiments/mem/table.py \
				  experiments/mem/mem.csv > experiments/mem/mem.tex

experiments/mem/c-mem.tex: experiments/lib.py experiments/mem/c-table.py \
	experiments/mem/c-mem.csv
	$(RE) experiments/mem/c-table.py \
					experiments/mem/c-mem.csv > experiments/mem/c-mem.tex

experiments/absolute/compare.tex: experiments/lib.py experiments/absolute/compare.py \
	experiments/mem/unoptimized-mem.csv experiments/absolute/runtime.csv
	$(RE) experiments/absolute/compare.py \
		experiments/absolute/runtime.csv experiments/absolute/unoptimized.csv \
		experiments/mem/mem.csv experiments/mem/unoptimized-mem.csv > \
		experiments/absolute/compare.tex

clean:
	rm -f thesis.pdf *.bbl *.blg *.log *.lot \
		*.brf *.lof *.toc *.out \
		*.aux *.log
