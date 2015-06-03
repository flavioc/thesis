#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 2:
   print "usage: table.py <csv file>"
   sys.exit(1)

expsets = read_experiment_set(sys.argv[1])
try: threaded = expsets["th"]
except: threaded = None
try: c = expsets["c"]
except: c = None
try: py = expsets["python"]
except: py = None
try: gl = expsets["graphlab"]
except: gl = None

print "\\begin{tabular}{c | c || c | c | c} \\hline"
print "\t\\textbf{Program} & \\textbf{Size} & \\textbf{C++ Time} (s) & \\textbf{LM} & \\textbf{Other} \\\\ \\hline \\hline"

for name in threaded.experiment_names():
   datasets = threaded.experiment_datasets_for(name)

   print "\t",
   if len(datasets) > 1:
      print "\\multirow{" + str(len(datasets)) + "}{*}{" + name2title(name) + "}",
   else: print name2title(name),

   first = True
   for dataset in datasets:
      lmexp = threaded.get_experiment(name, dataset)
      cexp = c.get_experiment(name, dataset)

      try: pyexp = py.get_experiment(name, dataset)
      except KeyError: pyexp = None
      try: glexp = gl.get_experiment(name, dataset)
      except KeyError: glexp = None

      if first: first = False
      else: print "\t\t",

      print " & " + dataset2title(dataset, name) + " & ",
      print "%.2f" % float(cexp.get_time_seconds(1)),
      print " & ",
      print "%.2f" % float(lmexp.get_time(1) / cexp.get_time(1)),
      print " & ",

      if pyexp: print "%.2f (Python)" % float(pyexp.get_time(1) / cexp.get_time(1)),
      elif glexp: print "%.2f (GraphLab)" % float(glexp.get_time(1) / cexp.get_time(1)),
      else: print "-",

      print "\\\\"
   print "\t\\hline"

print "\\end{tabular}"
