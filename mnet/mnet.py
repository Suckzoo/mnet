import sys
sys.path.append('../')
from main import branch_distance, Toolbox, run_ga, variables, branches, normalize

from deap import tools

def branch_look_ahead(individual):
	count = len(branches)
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	for i in branches:
		if eval(i):
			count -= 1
	return count

def fitness(individual):
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	approach_lv = len(branches) - 1
	for i in branches:
		if eval(i):
			approach_lv -= 1
		else:
			return [approach_lv + normalize(branch_distance(individual, i)), branch_look_ahead(individual)]
	return [0, 0]

toolbox = Toolbox(2)
toolbox.toolbox.register("evaluate", fitness)
toolbox.toolbox.register("select", tools.selNSGA2)

run_ga(toolbox)
