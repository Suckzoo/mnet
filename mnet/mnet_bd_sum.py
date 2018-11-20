import sys
sys.path.append('../')

from main import generate_fitness, variables, branches, is_pass, branch_distance, run_nsga

def branch_all_sum(individual):
	bd_sum = 0
	for i in range(len(branches)):
		if not is_pass(individual, branches[i]):
			bd_sum += branch_distance(individual, branches[i]) 
	return bd_sum

def fitness(individual):
	return generate_fitness(individual, branch_all_sum)

run_nsga(fitness)

