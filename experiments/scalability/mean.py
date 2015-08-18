#!/usr/bin/python

import sys
from lib import *

if len(sys.argv) != 3:
   print "mean.py <csv file> <output file>"
   sys.exit(1)

csv_file = sys.argv[1]
output = sys.argv[2]

expsets = read_experiment_set(csv_file)
try:
   threaded = expsets["th"]
except:
   print "could not find", csv_file
   sys.exit(1)

experiments = threaded.get_all()
harmonic_plot(experiments, output)
