from mnet import generate_fitness, run_nsga, variables, branches

def branch_look_ahead(individual):
	count = len(branches)
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	for i in branches:
		if eval(i):
			count -= 1
	return count

def fitness(individual):
	return generate_fitness(individual, branch_look_ahead(individual))

run_nsga(fitness)

