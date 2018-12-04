import sys
sys.path.append('../')
sys.path.append('.')

from main import generate_fitness, variables, branches, is_pass, branch_distance, run_nsga

def branch_weight_sum(individual):
	bd_wg_sum = 0
	approach_lv = len(branches) - 1
	for i in range(len(branches)):
		if not is_pass(individual, branches[i]):
			bd_wg_sum += branch_distance(individual, branches[i]) * (approach_lv + 1)
		approach_lv -= 1
	return bd_wg_sum

def fitness(individual):
	return generate_fitness(individual, branch_weight_sum)

run_nsga(fitness)

