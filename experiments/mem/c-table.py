#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 2:
   print "usage: c-table.py <csv file>"
   sys.exit(1)

expsets = read_mem_experiment_set(sys.argv[1])
try:
   c = expsets["c"]
except:
   print "Failed to load th experiment set"
   sys.exit(1)

print "\\begin{tabular}{c | c | c | c} \\hline"
print "\t\\textbf{Program} & \\textbf{Size} & \\textbf{Average} & \\textbf{Final} \\\\ \\hline \\hline"

for name in c.experiment_names():
   datasets = c.experiment_datasets_for(name)

   print "\t",
   if len(datasets) > 1:
      print "\\multirow{" + str(len(datasets)) + "}{*}{" + name2title(name) + "}",
   else: print name2title(name),

   first = True
   for dataset in datasets:
      exp = c.get_experiment(name, dataset)

      if first: first = False
      else: print "\t\t",

      print " & " + dataset2title(dataset, name) + " & " + readable_mem(exp.get_total_memory_average(1)) + " & " + readable_mem(exp.get_total_memory(1)) + "\\\\"
   print "\t\\hline"

print "\\end{tabular}"
