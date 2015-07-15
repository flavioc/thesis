
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from operator import truediv
from matplotlib import rcParams
from numpy import nanmax

max_threads = 32

def dataset2title(dataset, name):
   if not dataset:
      return '-'
   table = {'2000': '2000 nodes',
            'search_engines': 'Search Engines',
            'uspowergrid': 'US Power Grid',
            '1000': '1000 nodes',
            '500': '500 nodes',
            '11': '11',
            '12': '12',
            '13': '13',
            '14': '14',
            'small': 'Small',
            'big': 'Big',
            '200': '200x200',
            '50': '50x50',
            '300': '300x300',
            '400': '400x400',
            '80': '80x80',
            '120': '120x120',
            'orkut': 'Orkut',
            'livejournal': 'Live Journal',
            'twitter': 'Twitter',
            'usairports500': 'US 500 Airports',
            'email': 'EU Email',
            'gplus': 'Google Plus',
            'oclinks': 'OCLinks',
            'pokec': 'Pokec Social Network',
            'celegans': 'Celegans',
            'hepph': 'Arxiv HEP-PH'}
   return table[dataset]

def move_from_list(dest, src, elem):
   try:
      idx = src.index(elem)
      src.pop(idx)
      dest.append(elem)
   except:
      return

def sort_datasets(name, l):
   if name == 'shortest':
      x = []
      move_from_list(x, l, 'usairports500')
      move_from_list(x, l, 'oclinks')
      move_from_list(x, l, 'email')
      move_from_list(x, l, 'twitter')
      move_from_list(x, l, 'uspowergrid')
      x.extend(l)
      return x
   if name == 'min-max-tictactoe':
      x = []
      move_from_list(x, l, 'small')
      move_from_list(x, l, 'big')
      x.extend(l)
      return x
   else:
      return l

def name2title(name):
   table = {'greedy-graph-coloring': 'Greedy Graph Coloring',
            'shortest': 'MSSD',
            '8queens': 'N-Queens',
            'tree': "Tree",
            'tree-coord': "Tree (coordinated)",
            'min-max-tictactoe': "MiniMax",
            'belief-propagation': "Belief Propagation",
            'splash-bp-400': "Belief Propagation (400x400 with Splashes)",
            'pagerank': 'PageRank',
            'new-heat-transfer': 'Heat Transfer'}
   return table[name]

def parse_name(name):
   if name.startswith('belief-propagation'):
      return 'belief-propagation'
   if name.startswith('new-heat-transfer'):
      return 'new-heat-transfer'
   if name.startswith('min-max-tictactoe'):
      return 'min-max-tictactoe'
   if name.startswith('8queens-'):
      return '8queens'
   if name.startswith('shortest-'):
      return 'shortest'
   if name.startswith('greedy-graph-coloring-'):
      return 'greedy-graph-coloring'
   if name.startswith('pagerank-'):
      return 'pagerank'
   raise name

def parse_dataset(name):
   if name == 'min-max-tictactoe':
      return 'small'
   vec = name.split('-')
   last = vec[len(vec)-1]
   return last

def coordinated_program(name):
   if name == 'belief-propagation-400':
      return 'splash-bp-400'
   return name + '-coord'

class experiment_set(object):
   def add_experiment(self, name, dataset, threads, time):
      threads = int(threads)
      try:
         exp = self.experiments[(name, dataset)]
         exp.add_time(threads, time)
      except KeyError:
         exp = experiment(name, dataset)
         self.experiments[(name, dataset)] = exp
         exp.add_time(threads, time)

   def add_mem_experiment(self, name, dataset, threads, vec):
      try:
         exp = self.experiments[(name, dataset)]
         exp.add_mem(threads, vec)
      except KeyError:
         exp = experiment(name, dataset)
         self.experiments[(name, dataset)] = exp
         exp.add_mem(threads, vec)

   def add_c_mem_experiment(self, name, dataset, threads, avg):
      try:
         exp = self.experiments[(name, dataset)]
         exp.add_total_memory_average(threads, avg)
      except KeyError:
         exp = experiment(name, dataset)
         self.experiments[(name, dataset)] = exp
         exp.add_total_memory_average(threads, avg)

   def experiment_names(self):
      s = {name:True for (name, dataset) in self.experiments.keys()}
      return sorted(s.keys(), key=name2title)

   def experiment_datasets_for(self, name):
      l = [dataset for (name2, dataset) in self.experiments.keys() if name == name2]
      l = sorted(l, key=lambda item: (int(item.partition(' ')[0])
                                        if len(item) > 0 and item[0].isdigit() else float('inf'), item))
      l = sort_datasets(name, l)
      return l

   def experiment_datasets(self):
      return [dataset for (name, dataset) in self.experiments.keys()]

   def get_experiment(self, name, dataset):
      try:
         return self.experiments[(name, dataset)]
      except KeyError:
         return None

   def create_histogram_compare(self, prefix, other, threads):
      n = len(self.experiments)
      ind = np.arange(n)
      width = 0.35

      fig, ax = plt.subplots()

      cmap = plt.get_cmap('gray')
      otherRect = ax.bar(ind, [1] * n, width, color=cmap(0.2))
      timesNew = list(x.get_time(threads) for x in self.experiments.values())
      timesOld = list(x.get_time(threads) for x in other.experiments.values())

      thisRect = ax.bar(ind + width, map(truediv, timesNew, timesOld), width, color=cmap(0.7))

      ax.set_ylabel('Relative Execution')
      title = 'Comparison (' + str(threads) + ' thread'
      if threads > 1:
         title += 's'
      title += ')'
      ax.set_title(title)
      ax.set_xticks(ind+width)
      ax.set_xticklabels(list(name2title(x) for x in self.experiments.keys()), rotation=45, fontsize=10, ha='right')
      ax.legend((otherRect[0], thisRect[0]), ('Old', 'New'))
      ax.set_ylim([0, 1.5])

      plt.tight_layout()
      name = prefix + "comparison" + str(threads) + ".png"
      plt.savefig(name)

   def __init__(self):
      self.experiments = {}

class experiment(object):

   def add_total_memory_average(self, nthreads, mem): self.total_memory_average[nthreads] = mem
   def get_total_memory_average(self, nthreads): return self.total_memory_average[nthreads]

   def add_total_memory(self, nthreads, mem): self.total_memory[nthreads] = mem
   def get_total_memory(self, nthreads): return self.total_memory[nthreads]

   def add_memory_in_use(self, nthreads, mem): self.memory_in_use[nthreads] = mem
   def get_memory_in_use(self, nthreads): return self.memory_in_use[nthreads]

   def add_num_mallocs(self, nthreads, mem): self.num_mallocs[nthreads] = mem
   def get_num_mallocs(self, nthreads): return self.num_mallocs[nthreads]

   def add_num_facts(self, nthreads, mem): self.num_facts[nthreads] = mem
   def get_num_facts(self, nthreads): return self.num_facts[nthreads]

   def add_mem(self, nthreads, vec):
      assert(len(vec) == 5)
      self.add_total_memory_average(nthreads, int(vec[0]))
      self.add_total_memory(nthreads, int(vec[1]))
      self.add_memory_in_use(nthreads, int(vec[2]))
      self.add_num_mallocs(nthreads, int(vec[3]))
      self.add_num_facts(nthreads, int(vec[4]))

   def add_time(self, nthreads, time):
      assert(nthreads)
      self.times[nthreads] = time
   def get_time(self, nthreads): return float(self.times[nthreads])
   def get_time_seconds(self, nthreads):
      return float(self.times[nthreads]) / 1000

   def x_axis(self):
      return self.x_axis1()

   def x_axis1(self):
      return [key for key in sorted(self.times) if key <= max_threads]

   def base_speedup_data(self, base=None):
      if not base:
         base = self.times[1]
      return [float(base)/float(self.times[th]) for th in sorted(self.times) if th <= max_threads]

   def speedup_data(self, base=None):
      return [None] + self.base_speedup_data(base)

   def time_data(self):
      return [float(self.times[th]) for th in sorted(self.times) if th <= max_threads]

   def linear_speedup(self):
      return self.x_axis()

   def max_speedup(self, base=None):
      if not base:
         base = self.times[1]
      m = max(float(base)/float(x) for th, x in self.times.iteritems() if th <= max_threads)
      if m <= 16:
         return math.ceil(m) + 1
      else:
         return math.ceil(m) + 2

   def max_time(self):
      m = max(x for th, x in self.times.iteritems() if th <= max_threads)
      return float(m) * 1.1

   def get_improvement(self, reg):
      return [float(reg.get_time(th))/float(c) for th, c in self.times.iteritems() if th <= max_threads]

   def create_coord_improv(self, prefix, coordinated):
      fig = plt.figure()
      ax = fig.add_subplot(111)

      names = ('Improvement')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax.set_title(self.title, fontsize=titlefontsize)
      ax.yaxis.tick_right()
      ax.yaxis.set_label_position("right")
      ax.set_ylabel('Improvement', fontsize=ylabelfontsize)
      ax.set_xlabel('Threads', fontsize=ylabelfontsize)
      max_value_threads = max(x for x in self.times.keys() if x <= max_threads)
      improvs = coordinated.get_improvement(self)
      ax.set_xlim([1, max_value_threads])
      ax.set_ylim([0, math.ceil(max(improvs))])

      cmap = plt.get_cmap('gray')

      ax.plot(self.x_axis1(), improvs,
         label='Coordination', linestyle='--', marker='^', color=cmap(0.1))
# ax.legend([reg, coord], ["Regular", "Coordinated"], loc=2, fontsize=20, markerscale=2)

      setup_lines(ax, cmap)

      name = prefix + self.name + ".png"
      plt.savefig(name)

   def create_queens(self, c, top, top_static, bottom, bottom_static):
      fig = plt.figure()
      ax1 = fig.add_subplot(111)
      ax2 = ax1.twinx()
      baseline = c.get_time(1)

      names = ('Speedup')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax2.set_title(self.title, fontsize=titlefontsize)
      ax2.set_ylabel('C/V Speedup', fontsize=ylabelfontsize)
      ax2.set_xlabel('Threads', fontsize=ylabelfontsize)
      max_value_threads = max(x for x in self.times.keys() if x <= max_threads)
      mspeedup = max(self.max_speedup(baseline), top.max_speedup(baseline))
      ax2.set_xlim([0, max_value_threads])
      ax2.set_ylim([0, mspeedup])

      cmap = plt.get_cmap('gray')

      reg, = ax2.plot(self.x_axis(), self.speedup_data(baseline),
         linestyle='--', marker='^', color=cmap(0.1))
      topg, = ax2.plot(self.x_axis(), top.speedup_data(baseline),
         linestyle='--', marker='s', color=cmap(0.4))
      top_staticg, = ax2.plot(self.x_axis(), top_static.speedup_data(baseline),
         linestyle='--', marker='o', color=cmap(0.4))
      bottomg, = ax2.plot(self.x_axis(), bottom.speedup_data(baseline),
            linestyle='--', marker='x', color=cmap(0.4))
      bottom_staticg, = ax2.plot(self.x_axis(), bottom_static.speedup_data(baseline),
            linestyle='--', marker='D', color=cmap(0.4))

      ax1.plot(self.x_axis(), self.linear_speedup(),
        label='Linear', linestyle='-', color=cmap(0.2))
      ax1.set_ylabel("Reg1/Top Speedup", fontsize=ylabelfontsize)
      base = self.get_time(1)
      ax1.set_ylim([0, top.max_speedup(base)])
      topreg, = ax1.plot(top.x_axis(), top.speedup_data(base),
            linestyle='--', color=cmap(0.3))

      ax2.legend([reg, topg, top_staticg, bottomg, bottom_staticg, topreg], ["C/Regular",
            "C/Top", "C/Top Static", "C/Bottom", "C/Bottom Static", "Reg1/Top"], loc=2, fontsize=18, markerscale=2)

      setup_lines(ax1, cmap)
      setup_lines(ax2, cmap)

      name = self.name + ".png"
      plt.savefig(name)

   def create_ht(self, baseline, coord, localonly):
      fig = plt.figure()
      ax1 = fig.add_subplot(111)
      ax2 = ax1.twinx()

      names = ('Speedup')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax2.set_title(self.title, fontsize=titlefontsize)
      ax2.set_ylabel('C/V Speedup', fontsize=ylabelfontsize)
      ax2.set_xlabel('Threads', fontsize=ylabelfontsize)
      max_value_threads = max(x for x in self.times.keys() if x <= max_threads)

      base = baseline.get_time(1)
      mspeedup = max(self.max_speedup(base), localonly.max_speedup(base))
      ax2.set_xlim([0, max_value_threads])
      ax2.set_ylim([0, mspeedup])

      cmap = plt.get_cmap('gray')

      reg, = ax2.plot(self.x_axis(), self.speedup_data(base),
         linestyle='--', marker='^', color=cmap(0.1))
      coordx, = ax2.plot(self.x_axis(), coord.speedup_data(base),
         linestyle='--', marker='s', color=cmap(0.4))
      lo, = ax2.plot(self.x_axis(), localonly.speedup_data(base),
         linestyle='--', marker='D', color=cmap(0.4))

      ax1.plot(self.x_axis(), self.linear_speedup(),
        label='Linear', linestyle='-', color=cmap(0.2))
      ax1.set_ylabel("Reg1/Local Speedup", fontsize=ylabelfontsize)
      base = self.get_time(1)
      ax1.set_ylim([0, localonly.max_speedup(base)])
      localreg, = ax1.plot(coord.x_axis(), localonly.speedup_data(base),
            linestyle='--', color=cmap(0.3))

      ax2.legend([reg, coordx, lo, localreg], ["C/Regular",
            "C/Coordinated", "C/Local", "Reg1/Local"], loc=2, fontsize=18, markerscale=2)

      setup_lines(ax2, cmap)
      setup_lines(ax1, cmap)

      name = self.name + ".png"
      plt.savefig(name)

   def create_coord(self, prefix, coordinated, baseline):
      fig = plt.figure()
      ax1 = fig.add_subplot(111)
      ax2 = ax1.twinx()

      names = ('Speedup')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax2.set_title(self.title, fontsize=titlefontsize)
      ax2.set_ylabel('C/V Speedup', fontsize=ylabelfontsize)
      ax2.set_xlabel('Threads', fontsize=ylabelfontsize)
      max_value_threads = max(x for x in self.times.keys() if x <= max_threads)
      base = baseline.get_time(1)
      mspeedup = max(self.max_speedup(base), coordinated.max_speedup(base))
      ax2.set_xlim([0, max_value_threads])
      ax2.set_ylim([0, mspeedup])

      cmap = plt.get_cmap('gray')

      reg, = ax2.plot(self.x_axis(), self.speedup_data(base),
         linestyle='--', marker='^', color=cmap(0.1))
      coord, = ax2.plot(self.x_axis(), coordinated.speedup_data(base),
         linestyle='--', marker='s', color=cmap(0.4))

      ax1.plot(self.x_axis(), self.linear_speedup(),
        label='Linear', linestyle='-', color=cmap(0.2))

      ax1.set_ylabel("Reg1/Coord Speedup", fontsize=ylabelfontsize)
      base = self.get_time(1)
      ax1.set_ylim([0, coordinated.max_speedup(base)])
      coordreg, = ax1.plot(coordinated.x_axis(), coordinated.speedup_data(base),
            linestyle='--', color=cmap(0.3))

      ax2.legend([reg, coord, coordreg], ["C/Regular",
            "C/Coordinated", "Reg1/Coord"], loc=2, fontsize=20, markerscale=2)

      setup_lines(ax2, cmap)
      setup_lines(ax1, cmap)

      name = prefix + self.name + ".png"
      plt.savefig(name)

   def max_threads(self):
      return max(x for x in self.times.keys() if x <= max_threads)

   def allocator_compare(self, other_exp, prefix, stdname, othername):
      fig = plt.figure()
      ax = fig.add_subplot(111)
      ax2 = ax.twinx()

      names = ('Scalability')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax.set_title(self.title, fontsize=titlefontsize)
      ax.yaxis.tick_left()
      ax.yaxis.set_label_position("left")
      ax.set_ylabel('Execution Time', fontsize=ylabelfontsize)
      ax.set_xlabel('Threads', fontsize=ylabelfontsize)
      ax2.set_ylabel('Speedup', fontsize=ylabelfontsize)
      ax.set_xlim([1, self.max_threads()])
      ax.set_ylim([0, max(self.max_time(), other_exp.max_time())])
      cmap = plt.get_cmap('gray')

      stdtime, = ax.plot(self.x_axis(), self.time_data(),
         label='Standard Allocator Run Time', linestyle='-', marker='+', color='r')
      othertime, = ax.plot(self.x_axis(), other_exp.time_data(),
         label='Other Allocator Run Time', linestyle='--', marker='o', color='g')
      stdspeedup, = ax2.plot(self.x_axis(), self.base_speedup_data(),
            label='Standard Allocator Speedup', linestyle='--', marker='+', color='r')
      otherspeedup, = ax2.plot(self.x_axis(), other_exp.base_speedup_data(),
            label='Other Allocator Speedup', linestyle='-', marker='o', color='g')
      ax.legend([(stdtime, stdspeedup), (othertime, otherspeedup)], [stdname, othername],
            loc=2, fontsize=18, markerscale=2)

      setup_lines(ax, cmap)
      setup_lines(ax2, cmap)

      name = prefix + self.create_filename()
      plt.savefig(name)

   def create_scale(self, cexp, prefix):
      fig = plt.figure()
      ax = fig.add_subplot(111)
      ax2 = ax.twinx()

      names = ('Scalability')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax.set_title(self.title, fontsize=titlefontsize)
      ax.yaxis.tick_left()
      ax.yaxis.set_label_position("left")
      ax2.yaxis.tick_right()
      ax2.set_ylabel('Speedup', fontsize=ylabelfontsize, color='g')
      ax2.set_ylim([0, self.max_speedup()])
      ax.set_ylabel('Execution Time', fontsize=ylabelfontsize, color='r')
      ax.set_xlabel('Threads', fontsize=ylabelfontsize)
      ax.set_xlim([1, self.max_threads()])
      ax.set_ylim([0, self.max_time()])
      cmap = plt.get_cmap('gray')

      ax.spines['left'].set_color('red')
      ax2.spines['left'].set_color('red')
      ax.spines['right'].set_color('green')
      ax2.spines['right'].set_color('green')
      [t.set_color('red') for t in ax.yaxis.get_ticklabels()]
      [t.set_color('green') for t in ax2.yaxis.get_ticklabels()]

      ax.plot(self.x_axis(), self.time_data(),
         label='Execution Time', linestyle='--', marker='+', color='r')
      ax2.plot(self.x_axis(), self.base_speedup_data(),
         label='Speedup', linestyle='--', marker='o', color='g')
      if cexp:
         ax.plot(self.x_axis(), [cexp.get_time(1)] * len(self.x_axis()),
           label='Linear', linestyle='-', color=cmap(0.2))

      setup_lines(ax, cmap)
      setup_lines(ax2, cmap)

      name = prefix + self.create_filename()
      plt.savefig(name)

   def create_filename(self):
      s = self.name
      if self.dataset:
         s = s + "-" + self.dataset
      return s + ".png"

   def create_comparison_coord_system(self, prefix, coord, system, coord_system, system_name='GraphLab', title=None):
      fig = plt.figure()
      ax = fig.add_subplot(111)

      names = ('Speedup')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      if not title:
         title = "Coordination Improvement"
      ax.set_title(title, fontsize=titlefontsize)
      ax.yaxis.tick_right()
      ax.yaxis.set_label_position("right")
      ax.set_ylabel('Improvement', fontsize=ylabelfontsize)
      ax.set_xlabel('Threads', fontsize=ylabelfontsize)
      max_value_threads = max(x for x in self.times.keys() if x <= max_threads)
      improv_lm = coord.get_improvement(self)
      improv_system = coord_system.get_improvement(system)
      ax.set_xlim([1, max_value_threads])
      ax.set_ylim([0, math.ceil(max(max(improv_lm), max(improv_system))) + 1])

      cmap = plt.get_cmap('gray')

      lm, = ax.plot(self.x_axis1(), improv_lm,
         label='CLM Improvement', linestyle='--', marker='^', color=cmap(0.1))
      other, = ax.plot(self.x_axis1(), improv_system,
         label=system_name + ' Improvement', linestyle='--', marker='+', color=cmap(0.6))
      ax.legend([lm, other], ["CLM", system_name], loc=2, fontsize=20, markerscale=2)

      setup_lines(ax, cmap)

      name = prefix + "improve_" + self.name + ".png"
      plt.savefig(name)


   def create_speedup_compare_systems(self, prefix, system, system_name='GraphLab', title=None):
      fig = plt.figure()
      ax = fig.add_subplot(111)

      names = ('Speedup')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      if not title:
         title = self.title
      ax.set_title(title, fontsize=titlefontsize)
      ax.yaxis.tick_right()
      ax.yaxis.set_label_position("right")
      ax.set_ylabel('Speedup', fontsize=ylabelfontsize)
      ax.set_xlabel('Threads', fontsize=ylabelfontsize)
      max_value_threads = max(x for x in self.times.keys() if x <= max_threads)
      ax.set_xlim([0, max_value_threads])
      ax.set_ylim([0, max(self.max_speedup(), system.max_speedup())])

      cmap = plt.get_cmap('gray')

      lm, = ax.plot(self.x_axis(), self.speedup_data(),
         label='LM Speedup', linestyle='--', marker='^', color=cmap(0.1))
      other, = ax.plot(self.x_axis(), system.speedup_data(),
         label=system_name + ' Speedup', linestyle='--', marker='+', color=cmap(0.6))
      ax.plot(self.x_axis(), self.linear_speedup(),
        label='Linear', linestyle='-', color=cmap(0.2))
      ax.legend([lm, other], ["CLM", system_name], loc=2, fontsize=20, markerscale=2)

      setup_lines(ax, cmap)

      name = prefix + self.name + ".png"
      plt.savefig(name)

   def coordination_compare(self, coord_exp, cexp, prefix):
      fig = plt.figure()
      ax = fig.add_subplot(111)
      ax2 = ax.twinx()

      names = ('Scalability')
      formats = ('f4')
      titlefontsize = 22
      ylabelfontsize = 20
      ax.set_title(self.title, fontsize=titlefontsize)
      ax.yaxis.tick_left()
      ax.yaxis.set_label_position("left")
      ax.set_ylabel('Execution Time', fontsize=ylabelfontsize)
      ax.set_xlabel('Threads', fontsize=ylabelfontsize)
      ax2.set_ylabel('Speedup', fontsize=ylabelfontsize)
      ax.set_xlim([1, self.max_threads()])
      ax.set_ylim([0, max(self.max_time(), coord_exp.max_time())])
      cmap = plt.get_cmap('gray')

      regtime, = ax.plot(self.x_axis(), self.time_data(),
         label='Regular Run Time', linestyle='-', marker='+', color='r')
      coordtime, = ax.plot(self.x_axis(), coord_exp.time_data(),
         label='Coordinated Run Time', linestyle='--', marker='o', color='g')
      coordspeedup, = ax2.plot(self.x_axis(), coord_exp.base_speedup_data(self.get_time(1)),
            label='Coordinated Speedup', linestyle='--', marker='+', color='g')
      if cexp:
         ctime, = ax.plot(self.x_axis(), [cexp.get_time(1)] * len(self.x_axis()),
           label='Linear', linestyle='-', color=cmap(0.2))

      lines = [(regtime), coordtime, coordspeedup]
      labels = ["Regular", "Coordinated", "Regular(1)/Coordinated(t)"]
      if cexp:
        lines.append(ctime)
        labels.append("C++")

      ax.legend(lines, labels, loc=2, fontsize=18, markerscale=2)

      setup_lines(ax, cmap)
      setup_lines(ax2, cmap)

      name = prefix + self.create_filename()
      plt.savefig(name)

   def __init__(self, name, dataset):
      self.name = name
      self.dataset = dataset
      self.title = name2title(name)
      if dataset:
         self.title = self.title + " (" + dataset2title(dataset, name) + ")"
      self.times = {}
      self.total_memory_average = {}
      self.total_memory = {}
      self.memory_in_use = {}
      self.num_mallocs = {}
      self.num_facts = {}


def setup_lines(ax, cmap):
   lines = ax.lines
   markersize = 20
   markerspace = 1
   c = cmap(0.5)

   for i, ln in enumerate(lines):
     ln.set_linewidth(4)
     ln.set_markersize(markersize)
     ln.set_markevery(markerspace)

SPECIAL_SYSTEMS = ["c", "python", "graphlab", "ligra"]

def parse_threads(sched):
   if sched in SPECIAL_SYSTEMS: return 1
   else: return int(sched[2:])

def parse_sched(sched):
   if sched in SPECIAL_SYSTEMS: return sched
   else: return "th"

def read_experiment_set(filename):
   expsets = {}
   with open(filename, "r") as fp:
      for line in fp:
         line = line.rstrip("\n")
         if line == "": continue
         if line.startswith("#") or line.startswith(";"): continue
         vec = line.split(" ")
         if len(vec) < 2: continue
         first = vec[0]
         sched = vec[1]
         threads = parse_threads(sched)
         sched = parse_sched(sched)
         if first.endswith("-coord"):
            first = first[:-len("-coord")]
            sched = "coord"
         name = parse_name(first)
         dataset = parse_dataset(first)
         time = int(vec[len(vec)-1])
         #print name, sched, threads, dataset
         try:
            exp = expsets[sched]
         except KeyError:
            exp = experiment_set()
            expsets[sched] = exp
         exp.add_experiment(name, dataset, threads, time)
   return expsets

def read_mem_experiment_set(filename):
   expsets = {}
   with open(filename, "r") as fp:
      for line in fp:
         line = line.rstrip("\n").lstrip(" ").rstrip(" ")
         if line == "": continue
         if line.startswith("#") or line.startswith(";"): continue
         vec = line.split(" ")
         if len(vec) < 2: continue
         first = vec[0]
         sched = vec[1]
         threads = parse_threads(sched)
         sched = parse_sched(sched)
         if first.endswith("-coord"):
            first = first[:-len("-coord")]
            sched = "coord"
         name = parse_name(first)
         dataset = parse_dataset(first)
         rest = vec[2:]
         try:
            exp = expsets[sched]
         except KeyError:
            exp = experiment_set()
            expsets[sched] = exp
         if sched == 'c':
            exp.add_c_mem_experiment(name, dataset, 1, int(rest[0]))
         else:
            exp.add_mem_experiment(name, dataset, threads, rest)
   return expsets

def next_readable(s):
   if s == '':
      return 'K'
   elif s == 'K':
      return 'M'
   elif s == 'M':
      return 'G'
   elif s == 'G':
      return 'T'

def readable_number(num, start, extension, div):
   if num > 2000:
      return readable_number(num / div, next_readable(start), extension, div)
   else:
      return str(num) + start + extension

def readable_mem(num):
   return readable_number(num, 'K', 'B', 1024)

def readable_decimal(num): return readable_number(num, '', '', 1000)
