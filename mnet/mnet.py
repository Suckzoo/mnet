import sys
sys.path.append('../')
from main import variables, branch_distance, Toolbox, run_ga, branches, normalize, is_pass

from deap import tools

def generate_fitness(individual, second_fitness):
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	approach_lv = len(branches) - 1
	for i in branches:
		if eval(i):
			approach_lv -= 1
		else:
			return [approach_lv + normalize(branch_distance(individual, i)), second_fitness] 
	return [0, 0]

def run_nsga(fitness):
	toolbox = Toolbox(2)
	toolbox.toolbox.register("evaluate", fitness)
	toolbox.toolbox.register("select", tools.selNSGA2)
	run_ga(toolbox)

