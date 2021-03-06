#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 3:
   print "usage: thread-stats-table.py <csv file> <title>"
   sys.exit(1)

expsets = read_stats_experiment_set(sys.argv[1])
try: regs = expsets["th"]
except: sys.exit(1)
try: coords = expsets["coord"]
except:
   try:
      coords = expsets["threads"]
   except:
      sys.exit(1)

coord_name = sys.argv[2]
print "\\begin{tabular}{c | c || c c | c c | c c} \\hline"
print "\t \\multirow{2}{*}{\\textbf{Dataset}} & \\multirow{2}{*}{\\textbf{Threads}} & \\multicolumn{2}{c|}{\\textbf{\# Derived}} & \\multicolumn{2}{c|}{\\textbf{\# Deleted}} & \\multicolumn{2}{c}{\\textbf{\# Final}}\\\\"
print "\t & & Regular & " + coord_name + " & Regular & " + coord_name + " & Regular & " + coord_name + "\\\\ \\hline \\hline"

ALLOWED_THREADS = [1, 2, 4, 8, 16, 24, 32]
for name in regs.experiment_names():
   datasets = regs.experiment_datasets_for(name)

   for dataset in datasets:
      threads = regs.threads_for_experiment(name, dataset)
      threads = set(threads).intersection(ALLOWED_THREADS)
      title = dataset2title(dataset, name)
      if title == '1M C / 4000 G / Low Variability':
         title = '\\makecell{1M C / 4000 G \\\\Low Variability}'
      if title == '1M C / 4000 G / High Variability':
         title = '\\makecell{1M C / 4000 G \\\\High Variability}'
      print "\\multirow{" + str(len(threads)) + "}{*}{" + title + "}",
      reg = regs.get_experiment(name, dataset)
      coord = coords.get_experiment(name, dataset)

      for th in sorted(threads):
         print " & " + str(th) + " & ",
         print readable_decimal(reg.get_facts_derived(th)), "&",
         print readable_percentage((float(coord.get_facts_derived(th)) / float(reg.get_facts_derived(th))) * 100), "&",
         print readable_decimal(reg.get_facts_deleted(th)), "&",
         print readable_percentage((float(coord.get_facts_deleted(th)) / float(reg.get_facts_deleted(th))) * 100), "&",
         print readable_decimal(reg.get_num_facts(th)), "&",
         print readable_decimal(coord.get_num_facts(th)),
         print "\\\\"
      print "\t\\hline"

print "\\end{tabular}"
