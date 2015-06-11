#!/usr/bin/python

from lib import *
import sys

if len(sys.argv) != 4:
   print "usage: plot.py <thread csv file> <absolute csv file> <prefix>"
   sys.exit(1)

expsets = read_experiment_set(sys.argv[1])
try: threaded = expsets["th"]
except: sys.exit(1)
absolutesets = read_experiment_set(sys.argv[2])
try: c = absolutesets["c"]
except:
   print "failed to get c experiments"
   sys.exit(1)

for name in threaded.experiment_names():
   datasets = threaded.experiment_datasets_for(name)

   for dataset in datasets:
      lmexp = threaded.get_experiment(name, dataset)
      cexp = c.get_experiment(name, dataset)
      lmexp.create_scale(cexp, sys.argv[3] + "scale-")

