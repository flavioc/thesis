#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 3:
   print "usage: stats-table.py <regular csv file> <coordinated csv file>"
   sys.exit(1)

regexpsets = read_stats_experiment_set(sys.argv[1])
try: reg = regexpsets["th"]
except: sys.exit(1)
coordexpsets = read_stats_experiment_set(sys.argv[2])
try: coord = coordexpsets["coord"]
except: sys.exit(1)

print "\\begin{tabular}{c || c | c | c | c | c | c | c} \\hline"
print "\t\\textbf{Dataset} & \\multicolumn{2}{c|}{\\textbf{\# Derived}} & \\multicolumn{2}{c|}{\\textbf{\# Sent}} & \\multicolumn{2}{c|}{\\textbf{\# Deleted}} & \\textbf{\# Final} \\\\ \\hline \\hline"

def do_experiment_set(expset, coordexpset):
   for name in expset.experiment_names():
      datasets = expset.experiment_datasets_for(name)

      if len(datasets) > 1:
         #print "\\multirow{" + str(len(datasets)) + "}{*}{" + expname + "}",
         pass

      for dataset in datasets:
         lmexp = expset.get_experiment(name, dataset)
         coordexp = coordexpset.get_experiment(name, dataset)

         print dataset2title(dataset, name) + " & " + readable_decimal(lmexp.get_facts_derived(1)),
         print " & ",
         print readable_percentage(int(float(coordexp.get_facts_derived(1)) / float(lmexp.get_facts_derived(1)) * 100)),
         print  " & " + readable_decimal(lmexp.get_facts_sent(1)) + " & ",
         print readable_percentage(int(float(coordexp.get_facts_sent(1)) / float(lmexp.get_facts_sent(1)) * 100)),
         print  " & " + readable_decimal(lmexp.get_facts_deleted(1)) + " & ",
         print readable_percentage(int(float(coordexp.get_facts_deleted(1)) / float(lmexp.get_facts_deleted(1)) * 100)),
         print " & " + readable_decimal(lmexp.get_num_facts(1)),
         print "\\\\"
      print "\t\\hline"

do_experiment_set(reg, coord)

print "\\end{tabular}"
