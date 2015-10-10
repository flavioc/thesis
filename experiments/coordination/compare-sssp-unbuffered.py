#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) < 7:
   print "usage: compare-sssp-unbuffered.py <regular runtime> <coordinated runtime> <sequential runtime> <ligra runtime> <unbuffered runtime> <prefix>"
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

ligra_sets = read_experiment_set(sys.argv[4])
try: ligra_set = ligra_sets["ligra"]
except: sys.exit(1)

unbuffered_sets = read_experiment_set(sys.argv[5])
try: unbuffered_set = unbuffered_sets["coord"]
except: sys.exit(1)

prefix = sys.argv[6]

for name in regular_threaded.experiment_names():
   datasets = regular_threaded.experiment_datasets_for(name)

   for dataset in datasets:
      regular_exp = regular_threaded.get_experiment(name, dataset)
      coord_exp = coord_threaded.get_experiment(name, dataset)
      c_exp = cexp_set.get_experiment(name, dataset)
      ligra_exp = ligra_set.get_experiment(name, dataset)
      unbuffered_exp = unbuffered_set.get_experiment(name, dataset)
      if regular_exp and coord_exp and ligra_exp and unbuffered_exp:
         base_time = unbuffered_exp.get_time(1)
         regular_exp.coordination_compare_with_base(coord_exp, c_exp, prefix, "UnOptimized", {"Ligra Time": ligra_exp}, base_time, "Coordinated")

sys.exit(0)
