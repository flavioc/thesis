#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) != 7:
   print "usage: splash-bp.py <bp csv> <sbp csv> <graphlab fifo csv> <graphlab multi csv> <graphlab splash csv> <prefix"
   sys.exit(1)

try:
   bpexpsets = read_experiment_set(sys.argv[1])
   bpthreaded = bpexpsets["th"]
   bp = bpthreaded.get_experiment('belief-propagation', '400')
except:
   print 'could not find belief-propagation in file', sys.argv[1]
   sys.exit(1)

try:
   sbpexpsets = read_experiment_set(sys.argv[2])
   sbpthreaded = sbpexpsets["th"]
   sbp = sbpthreaded.get_experiment('splash-bp', '400')
except:
   print 'could not find splash-bp in file', sys.argv[2]
   sys.exit(1)

try:
   glexpsets = read_experiment_set(sys.argv[3])
   glthreaded = glexpsets["gl"]
   glfifobp = glthreaded.get_experiment('belief-propagation', '400')
except:
   print "could not find graphlab fifo in file", sys.argv[3]
try:
   glexpsets = read_experiment_set(sys.argv[4])
   glthreaded = glexpsets["gl"]
   glmultibp = glthreaded.get_experiment('belief-propagation', '400')
except:
   print "could not find graphlab fifo in file", sys.argv[4]

try:
   glexpsets = read_experiment_set(sys.argv[5])
   glthreaded = glexpsets["gl"]
   glsbp = glthreaded.get_experiment('splash-bp', '400')
except:
   print 'could not find graphlab data in file', sys.argv[5]
   sys.exit(1)

assert(bp)
assert(sbp)
prefix = sys.argv[6]

bp.compare_graphlab(glfifobp, prefix + "fifo-")
bp.compare_graphlab(glmultibp, prefix + "multi-")
sbp.compare_graphlab(glsbp, prefix)
bp.compare_splashbp(sbp, glfifobp, glsbp, prefix + "ratio-fifo-")
bp.compare_splashbp(sbp, glmultibp, glsbp, prefix + "ratio-multi-")
