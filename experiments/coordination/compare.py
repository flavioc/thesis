#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) < 5:
   print "usage: compare.py <regular runtime> <coordinated runtime> <sequential runtime> <prefix> [name]"
   sys.exit(1)

regular_sets = read_experiment_set(sys.argv[1])
try: regular_threaded = regular_sets["th"]
except: sys.exit(1)

coord_sets = read_experiment_set(sys.argv[2])
try: coord_threaded = coord_sets["coord"]
except: sys.exit(1)

seq_sets = read_experiment_set(sys.argv[3])
try: cexp_set = seq_sets["c"]
except: sys.exit(1)


for name in regular_threaded.experiment_names():
   datasets = regular_threaded.experiment_datasets_for(name)

   for dataset in datasets:
      regular_exp = regular_threaded.get_experiment(name, dataset)
      coord_exp = coord_threaded.get_experiment(name, dataset)
      c_exp = cexp_set.get_experiment(name, dataset)
      if regular_exp and coord_exp:
         if len(sys.argv) == 6:
            name_used = sys.argv[5]
         else:
            name_used = None
         regular_exp.coordination_compare(coord_exp, c_exp, sys.argv[4], name_used)

sys.exit(0)
