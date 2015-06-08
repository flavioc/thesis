#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) != 5:
   print "compare.py <optimized> <unoptimized> <optimized mem> <unoptimized mem>"
   sys.exit(1)

expopt0 = read_experiment_set(sys.argv[1])
try: opt = expopt0["th"]
except: sys.exit(1)
expunopt0 = read_experiment_set(sys.argv[2])
try: unopt = expunopt0["th"]
except: sys.exit(1)

memopt0 = read_mem_experiment_set(sys.argv[3])
try: memopt = memopt0["th"]
except: sys.exit(1)
memunopt0 = read_mem_experiment_set(sys.argv[4])
try: memunopt = memunopt0["th"]
except: sys.exit(1)

print "\\begin{tabular}{c | c || c | c} \\hline"
print "\t\\textbf{Program} & \\textbf{Size} & \\textbf{Run Time} & \\textbf{Average Memory}\\\\ \\hline \\hline"

for name in unopt.experiment_names():
   datasets = unopt.experiment_datasets_for(name)

   print "\t",
   if len(datasets) > 1:
      print "\\multirow{" + str(len(datasets)) + "}{*}{" + name2title(name) + "}",
   else: print name2title(name),

   first = True
   for dataset in datasets:
      oexp = opt.get_experiment(name, dataset)
      uexp = unopt.get_experiment(name, dataset)
      moexp = memopt.get_experiment(name, dataset)
      memunexp = memunopt.get_experiment(name, dataset)
      assert oexp
      assert uexp
      assert moexp
      assert memunexp

      if first: first = False
      else: print "\t\t",

      print " & " + dataset2title(dataset, name) + " & ",
      print "%.2f" % float(uexp.get_time(1) / oexp.get_time(1)),
      print " & ",
      print "%.2f" % float(float(moexp.get_total_memory_average(1)) / float(memunexp.get_total_memory_average(1)))
      print " ",

      print "\\\\"
   print "\t\\hline"

print "\\end{tabular}"
