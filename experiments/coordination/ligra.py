#!/usr/bin/python

import sys

if len(sys.argv) != 2:
   print "ligra.py <ligra csv>"
   sys.exit(1)

filename = sys.argv[1]

data = {}
for line in open(filename, "r"):
   line = line.lstrip().rstrip()
   if line == "":
      continue
   vec = line.split(' ')
   if len(vec) < 4:
      continue
   typ = vec[1]
   name = vec[0]
   total = int(vec[2])
   runtime = int(vec[3])
   if typ == "ligra1":
      data[name] = runtime
   onetime = data[name]
   speedup = float(runtime) / float(onetime)
   loadtime = total - runtime
   newloadtime = speedup * float(loadtime)
   corrected_time = runtime + int(newloadtime)
   print name, typ, corrected_time
