#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 3:
   print "usage: mem-table.py <regular csv file> <coord csv file>"
   sys.exit(1)

regexpsets = read_mem_experiment_set(sys.argv[1])
try:
   regexpsets = regexpsets["th"]
except:
   print "Failed to load th experiment set"
   sys.exit(1)
coordexpsets = read_mem_experiment_set(sys.argv[2])
try:
   coordexpsets = coordexpsets["coord"]
except:
   print "Failed to load coord experiment set"
   sys.exit(1)

print "\\begin{tabular}{c | c || c c | c c | c c} \\hline"
print "\t \\multirow{2}{*}{\\textbf{Dataset}} & \\multirow{2}{*}{\\textbf{Threads}} & \\multicolumn{2}{c|}{\\textbf{Average}} & \\multicolumn{2}{c|}{\\textbf{Final}} & \\multicolumn{2}{c}{\\textbf{\# Malloc}}\\\\"
print "\t & & Regular & Coord & Regular & Coord & Regular & Coord\\\\ \\hline \\hline"

ALLOWED_THREADS = [1, 2, 4, 8, 16, 24, 32]
for name in coordexpsets.experiment_names():
   datasets = coordexpsets.experiment_datasets_for(name)

   for dataset in datasets:
      threads = coordexpsets.threads_for_experiment(name, dataset)
      threads = set(threads).intersection(ALLOWED_THREADS)
      print "\\multirow{" + str(len(threads)) + "}{*}{" + dataset2title(dataset, name) + "}",
      for th in sorted(threads):
         reg = regexpsets.get_experiment(name, dataset)
         coord = coordexpsets.get_experiment(name, dataset)

         print " & " + str(th) + " & ",
         print readable_mem(reg.get_total_memory_average(th)) + " & " + readable_mem(coord.get_total_memory_average(th)) + " & ",
         print readable_mem(reg.get_memory_in_use(th)) + " & " + readable_mem(coord.get_memory_in_use(th)) + " & ",
         print readable_decimal(reg.get_num_mallocs(th)) + " & " + readable_decimal(coord.get_num_mallocs(th)) + "\\\\"
      
      print "\\hline"

print "\\end{tabular}"
