#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) != 4:
   print "usage: compare-alloc.py <regular allocator> <other allocator> <prefix>"
   sys.exit(1)

regular_sets = read_experiment_set(sys.argv[1])
try: regular_threaded = regular_sets["th"]
except: sys.exit(1)

other_sets = read_experiment_set(sys.argv[2])
try: other_threaded = other_sets["th"]
except: sys.exit(1)

for name in regular_threaded.experiment_names():
   datasets = regular_threaded.experiment_datasets_for(name)

   for dataset in datasets:
      regular_exp = regular_threaded.get_experiment(name, dataset)
      other_exp = other_threaded.get_experiment(name, dataset)
      if regular_exp and other_exp:
         regular_exp.allocator_compare(other_exp, sys.argv[3] + "-allocator-")

