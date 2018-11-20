import sys
sys.path.append('../')

from main import generate_fitness, variables, branches, branch_distance, run_ga, normalize

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

run_ga(fitness)
