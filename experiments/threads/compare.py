#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) != 3:
   print "usage: compare.py <runtime> <prefix>"
   sys.exit(1)

sets = read_experiment_set(sys.argv[1])
try: regular = sets["th"]
except: sys.exit(1)

try: thread = sets["threads"]
except:
   try:
      thread = sets["coord"]
   except KeyError:
      print "no threaded datasets"
      sys.exit(1)

for name in regular.experiment_names():
   datasets = regular.experiment_datasets_for(name)

   for dataset in datasets:
      regular_exp = regular.get_experiment(name, dataset)
      thread_exp = thread.get_experiment(name, dataset)
      regular_exp.threads_compare(thread_exp, None, sys.argv[2])

sys.exit(0)
