import sys
sys.path.append('../')
sys.path.append('.')

from main import generate_fitness, variables, branches, run_nsga

def branch_look_ahead(individual):
	count = len(branches)
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	for i in branches:
		if eval(i):
			count -= 1
	return count

def fitness(individual):
	return generate_fitness(individual, branch_look_ahead)

if __name__ == "__main__":
	run_nsga(fitness)

