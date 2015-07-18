#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) != 5:
   print "usage: queens.py <regular runtime> <queens coord runtime> <sequential runtime> <prefix>"
   sys.exit(1)

regular_sets = read_experiment_set(sys.argv[1])
try: regular_threaded = regular_sets["th"]
except: sys.exit(1)

coord_sets = read_experiment_set(sys.argv[2])
try: coord_threaded = coord_sets["th"]
except: sys.exit(1)

seq_sets = read_experiment_set(sys.argv[3])
try: cexp_set = seq_sets["c"]
except: sys.exit(1)

datasets = coord_threaded.experiment_datasets_for('8queens-top')
assert(datasets)
dataset = datasets[0]
regular_exp = regular_threaded.get_experiment('8queens', dataset)
top_exp = coord_threaded.get_experiment('8queens-top', dataset)
top_static_exp = coord_threaded.get_experiment('8queens-top-static', dataset)
bottom_exp = coord_threaded.get_experiment('8queens-bottom', dataset)
bottom_static_exp = coord_threaded.get_experiment('8queens-bottom-static', dataset)

assert(regular_exp and top_exp and top_static_exp and bottom_exp and bottom_static_exp)
c_exp = cexp_set.get_experiment('8queens', dataset)
assert(c_exp)
prefix = sys.argv[4]
regular_exp.coordination_compare(top_exp, c_exp, prefix + 'cmp-top-', 'Top', 30)
regular_exp.coordination_compare(top_static_exp, c_exp, prefix + 'cmp-top-static-', 'Top Static', 30)
regular_exp.coordination_compare(bottom_exp, c_exp, prefix + 'cmp-bottom-', 'Bottom', 30)
regular_exp.coordination_compare(bottom_static_exp, c_exp, prefix + 'cmp-bottom-static-', 'Bottom Static', 30)
