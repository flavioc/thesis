#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 2:
   print "usage: table.py <csv file>"
   sys.exit(1)

expsets = read_mem_experiment_set(sys.argv[1])
try:
   threaded = expsets["th"]
except:
   print "Failed to load th experiment set"
   sys.exit(1)

print "\\begin{tabular}{c | c || c | c | c || c c} \\hline"
print "\t\\textbf{Program} & \\textbf{Size} & \\textbf{Average} & \\textbf{Final} & \\textbf{\\# Facts} & \\textbf{Each} \\\\ \\hline \\hline"

for name in threaded.experiment_names():
   datasets = threaded.experiment_datasets_for(name)

   print "\t",
   if len(datasets) > 1:
      print "\\multirow{" + str(len(datasets)) + "}{*}{" + name2title(name) + "}",
   else: print name2title(name),

   first = True
   for dataset in datasets:
      lmexp = threaded.get_experiment(name, dataset)

      if first: first = False
      else: print "\t\t",

      print " & " + dataset2title(dataset, name) + " & " + readable_mem(lmexp.get_total_memory_average(1)) + " & " + readable_mem(lmexp.get_memory_in_use(1)) + " & " + readable_decimal(lmexp.get_num_facts(1)) + " & " + ("%.2f" % (float(lmexp.get_memory_in_use(1))/float(lmexp.get_num_facts(1)))) + "KB",

      print "\\\\"
   print "\t\\hline"

print "\\end{tabular}"
