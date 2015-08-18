
EXPERIMENT_FILES := experiments/absolute/runtime.tex \
	experiments/mem/mem.tex experiments/mem/c-mem.tex \
	experiments/absolute/compare-no-indexing.tex \
	experiments/absolute/compare-no-arrays.tex \
	experiments/coordination/sssp-stats.tex \
	experiments/coordination/minmax-mem.tex \
	experiments/threads/powergrid-stats.tex \
	experiments/threads/key-value-stats.tex \
	experiments/coordination/ligra-scale.csv

FIGURES := $(wildcard figures/btree/btree_trace*.pdf) \
	$(wildcard figures/message/message_trace*.pdf) \
	$(wildcard figures/visit/trace*.pdf) \
	$(wildcard figures/sssp/coord*.pdf) \
	$(wildcard figures/sssp/*.pdf) \
	$(wildcard figures/implementation/*.pdf) \
	$(wildcard figures/compiler/*.pdf) \
	$(wildcard experiments/scalability/*.png) \
	$(wildcard experiments/threads/*.png) \
	experiments/scalability/overview.png

all: thesis.pdf

thesis.pdf: thesis.tex packages.tex	thesis-cover.tex ack.tex \
		introduction.tex coordination.tex language/key_value.tex \
		language/syntax.tex language/pagerank.tex language/quicksort.tex \
		language/message_routing.tex language/graph_visit.tex \
		language/applications.tex language/related_work.tex \
		implementation.tex logic/related_work.tex \
		implementation/performance.tex \
		implementation/node.tex implementation/coord.tex \
		implementation/overview.tex implementation/comp.tex \
		implementation/parallelism.tex implementation/locks.tex \
		implementation/related_work.tex implementation/evaluation.tex \
		implementation/scale.tex implementation/allocator-compare.tex \
		implementation/fact-allocator.tex implementation/scale.tex \
		coordination/partitioning.tex coordination/scheduling.tex \
		coordination/ht.tex language/bipartite.tex \
		language/semantics.tex \
		coordination/proof_sssp.tex coordination/proof_queens.tex \
		coordination/proof_minimax.tex \
		background/coordination.tex \
		coordination/types.tex coordination/rationale.tex \
		coordination/coord_sssp.tex coordination/programs.tex \
		coordination/minimax.tex coordination/queens.tex \
		coordination/bp.tex coordination/related_work.tex \
		language.tex logic_foundations.tex threads/summary.tex \
		threads/key_value.tex \
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
		logic/lld.tex logic/hld.tex logic/sequent_calculus.tex \
		logic/linear_logic.tex local.tex \
		implementation/rule_engine.tex \
		$(wildcard hld/*.tex) \
		$(wildcard lld/*.tex) \
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
	experiments/mem/c-mem.csv experiments/mem/mem.csv
	$(RE) experiments/mem/c-table.py \
					experiments/mem/c-mem.csv \
					experiments/mem/mem.csv > experiments/mem/c-mem.tex

experiments/absolute/compare-no-indexing.tex: experiments/lib.py experiments/absolute/compare.py \
	experiments/mem/no-indexing-mem.csv experiments/absolute/runtime.csv \
	experiments/absolute/no-indexing.csv
	$(RE) experiments/absolute/compare.py \
		experiments/absolute/runtime.csv experiments/absolute/no-indexing.csv \
		experiments/mem/mem.csv experiments/mem/no-indexing-mem.csv > \
		experiments/absolute/compare-no-indexing.tex

experiments/absolute/compare-no-arrays.tex: experiments/lib.py experiments/absolute/compare.py \
	experiments/mem/no-arrays.csv experiments/absolute/runtime.csv \
	experiments/absolute/no-arrays.csv
	$(RE) experiments/absolute/compare.py \
		experiments/absolute/runtime.csv experiments/absolute/no-arrays.csv \
		experiments/mem/mem.csv experiments/mem/no-arrays.csv > \
		experiments/absolute/compare-no-arrays.tex

experiments/coordination/sssp-stats.tex: experiments/lib.py experiments/coordination/stats-table.py \
	experiments/coordination/sssp-regular-stats.csv \
	experiments/coordination/sssp-coord-stats.csv
	$(RE) experiments/coordination/stats-table.py \
		experiments/coordination/sssp-regular-stats.csv \
		experiments/coordination/sssp-coord-stats.csv > \
		experiments/coordination/sssp-stats.tex

experiments/coordination/minmax-mem.tex: experiments/lib.py experiments/coordination/mem-table.py \
	experiments/coordination/minmax-mem.csv \
	experiments/coordination/minmax-coord-mem.csv
	$(RE) experiments/coordination/mem-table.py \
		experiments/coordination/minmax-mem.csv \
		experiments/coordination/minmax-coord-mem.csv > \
		experiments/coordination/minmax-mem.tex

experiments/threads/powergrid-stats.tex: experiments/lib.py experiments/threads/thread-stats-table.py \
	experiments/threads/powergrid-stats.csv
	$(RE) experiments/threads/thread-stats-table.py \
		experiments/threads/powergrid-stats.csv Threads > \
		experiments/threads/powergrid-stats.tex

experiments/threads/key-value-stats.tex: experiments/lib.py experiments/threads/thread-stats-table.py \
	experiments/threads/key-value-stats.csv
	$(RE) experiments/threads/thread-stats-table.py \
		experiments/threads/key-value-stats.csv Cached > \
		experiments/threads/key-value-stats.tex

plots: scale allocator coord thread

scale:
	$(RE) experiments/scalability/plot.py \
		experiments/scalability/runtime.csv \
		experiments/absolute/runtime.csv experiments/scalability/
coord:
	$(RE) experiments/coordination/compare-sssp.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/sssp-coord.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/ligra-scale.csv \
		experiments/coordination/cmp-
	$(RE) experiments/coordination/compare.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/sssp-coord-unbuffered.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/unbuffered-
	$(RE) experiments/coordination/compare.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/minmax-coord.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/cmp-
	$(RE) experiments/coordination/compare.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/ht-coord0.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/cmp-
	$(RE) experiments/coordination/compare.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/ht-coord.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/cmpnew-
	$(RE) experiments/coordination/queens.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/queens.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/
	$(RE) experiments/coordination/queens.py \
		experiments/scalability/runtime.csv \
		experiments/coordination/queens13.csv \
		experiments/absolute/runtime.csv \
		experiments/coordination/

allocator:
	$(RE) experiments/scalability/compare-alloc.py \
		experiments/scalability/runtime.csv \
		experiments/scalability/malloc-results.csv \
		experiments/scalability/malloc \
		"Threaded Alloc" "Malloc"
	$(RE) experiments/scalability/compare-alloc.py \
		experiments/scalability/runtime.csv \
		experiments/scalability/mixed-node-results.csv \
		experiments/scalability/node \
		"Threaded Alloc" "Fact Alloc"
	$(RE) experiments/scalability/compare-alloc.py \
		experiments/scalability/runtime.csv \
		experiments/scalability/fact-allocator-no-refs.csv \
		experiments/scalability/no-refs \
		"Threaded Alloc" "Fact No Refs Alloc"

thread:
	$(RE) experiments/threads/splash-bp.py \
		experiments/scalability/runtime.csv \
		experiments/threads/splash-bp.csv \
		experiments/threads/graphlab-fifo.csv \
		experiments/threads/graphlab-multi.csv \
		experiments/threads/graphlab.csv \
		experiments/threads/cmp-
	$(RE) experiments/threads/compare.py \
		experiments/threads/search.csv \
		experiments/threads/cmp- \
		Threads
	$(RE) experiments/threads/compare.py \
		experiments/threads/powergrid.csv \
		experiments/threads/cmp- \
		Threads
	$(RE) experiments/threads/compare.py \
		experiments/threads/key-value.csv \
		experiments/threads/cmp- \
		Cached

experiments/coordination/ligra-scale.csv: experiments/coordination/ligra.csv \
	experiments/coordination/ligra.py
	python experiments/coordination/ligra.py experiments/coordination/ligra.csv > \
		experiments/coordination/ligra-scale.csv

experiments/scalability/overview.png: experiments/scalability/runtime.csv \
	experiments/lib.py experiments/scalability/mean.py
	$(RE) experiments/scalability/mean.py \
		experiments/scalability/runtime.csv \
		experiments/scalability/overview.png
	
clean:
	rm -f thesis.pdf *.bbl *.blg *.log *.lot \
		*.brf *.lof *.toc *.out \
		*.aux *.log
