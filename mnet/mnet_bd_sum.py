from mnet import generate_fitness, run_nsga, variables, branches, is_pass, branch_distance

def branch_all_sum(individual):
	bd_sum = 0
	for i in range(len(branches)):
		if not is_pass(individual, branches[i]):
			bd_sum += branch_distance(individual, branches[i]) 
	return bd_sum

def fitness(individual):
	return generate_fitness(individual, branch_all_sum(individual))

run_nsga(fitness)

