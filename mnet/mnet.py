import sys
sys.path.append('../')
from main import branch_distance, Toolbox, run_ga, variables, branches, normalize, is_pass

from deap import tools

# Try 1
def branch_look_ahead(individual):
	count = len(branches)
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	for i in branches:
		if eval(i):
			count -= 1
	return count

# Try 2
def branch_all_sum(individual):
	bd_sum = 0
	for i in range(len(branches)):
		if not is_pass(individual, branches[i]):
			bd_sum += branch_distance(individual, branches[i]) 
	return bd_sum

# Try 3
def branch_weight_sum(individual):
	bd_wg_sum = 0
	approach_lv = len(branches) - 1
	for i in range(len(branches)):
		if not is_pass(individual, branches[i]):
			bd_wg_sum += branch_distance(individual, branches[i]) * (approach_lv + 1)
		approach_lv -= 1
	return bd_wg_sum

def is_float(string):
	try:
		float(string)
		return True
	except:
		return False

def is_string_variable(string):
	operators = {'>', '>=', '<', '<=', '==', '+', '-', '*', '/'}
	for i in operators:
		if string == i:
			return False
	if is_float(string):
		return False
	else:
		return True

def branch_relation(br1, br2):
	del_space_br1 = br1.split()
	del_space_br2 = br2.split()
	
	variable_br1 = []
	variable_br2 = []

	for i in del_space_br1:
		if is_string_variable(i):
			variable_br1.append(i)
	
	for i in del_space_br2:
		if is_string_variable(i):
			variable_br2.append(i)
	
	variable_br1 = set(variable_br1)
	variable_br2 = set(variable_br2)


	return 1 - (len(variable_br1 - variable_br2) / len(variable_br1))

# Try 4
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

def fitness(individual):
	return generate_fitness(individual, branch_look_ahead(individual))
	#return generate_fitness(individual, branch_all_sum(individual))
	#return generate_fitness(individual, branch_weight_sum(individual))
	#return generate_fitness(individual, branch_look_ahead(individual) + fitness_branch_relation(individual))

toolbox = Toolbox(2)
toolbox.toolbox.register("evaluate", fitness)
toolbox.toolbox.register("select", tools.selNSGA2)

run_ga(toolbox)

