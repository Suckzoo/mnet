import sys
sys.path.append('../')
from main import branch_distance, Toolbox, run_ga, variables, branches, normalize

from deap import tools

def fitness(individual):
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	approach_lv = len(branches) - 1
	for i in branches:
		if eval(i):
			approach_lv -= 1
		else:
			return [approach_lv + normalize(branch_distance(individual, i))]
	return [0] 

toolbox = Toolbox(1)
toolbox.toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.toolbox.register("evaluate", fitness)

run_ga(toolbox)
