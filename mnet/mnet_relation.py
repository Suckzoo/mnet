import sys
sys.path.append('../')

from main import generate_fitness, variables, branches, run_nsga
from mnet_branch_no import branch_look_ahead

def variable_in_branch(branch):
	variable_br = []

	for elem in variables:
		if elem in branch:
			variable_br.append(elem)

	return set(variable_br)

def branch_relation(br1, br2):
	variable_br1 = variable_in_branch(br1)
	variable_br2 = variable_in_branch(br2)

	return 1 - (len(variable_br1 - variable_br2) / len(variable_br1))

def fitness_branch_relation(individual):
	bg_relation = 0
	fail_index = 0
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	for i in range(len(branches)):
		if not eval(branches[i]):
			fail_index = i
			break

	for i in range(len(branches) - fail_index - 1):
		branch = branches[len(branches) - 1 - i]
		if eval(branch):
			hello = branch_relation(branches[fail_index], branch)
			bg_relation += hello
		
	return bg_relation

def final_fitness(individual):
	return branch_look_ahead(individual) + fitness_branch_relation(individual)

def fitness(individual):
	return generate_fitness(individual, final_fitness)

run_nsga(fitness)

