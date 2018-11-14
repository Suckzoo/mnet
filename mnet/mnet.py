import random
from deap import base, creator, tools

IND_SIZE = 3
SELECTOR = "NSGA2"

# Now hardcoded, but later it will be replaced with data from the outside
variables = ['x', 'y', 'z']
# Now hardcoded, but later it will be replaced with data from the outside
branches = ['x + y + 2*z > 6', 'x < 10', 'y > 3', 'z < 1', 'x + y + z < 9']
#branches = ['x + y + 2*z > 6', 'x < 10', 'y > 3']

def normalize(bd):
	return 1 - pow(1.001, -bd)

def branch_distance(individual, branch):
	k = 0
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	if '>' in branch:
		branch_elem = branch.split('>')
		return eval(branch_elem[1] + ' - (' + branch_elem[0] + ')')
	elif '>=' in branch:
		branch_elem = branch.split('>=')
		return eval(branch_elem[1] + ' - (' + branch_elem[0] + ')')
	elif '<' in branch:
		branch_elem = branch.split('<')
		return eval(branch_elem[0] + ' - (' + branch_elem[1] + ')')
	elif '<=' in branch:
		branch_elem = branch.split('<=')
		return eval(branch_elem[0] + ' - (' + branch_elem[1] + ')')
	elif '==' in branch:
		branch_elem = branch.split('==')
		return abs(eval(branch_elem[0] + ' - (' + branch_elem[1] + ')'))
	elif '!=' in branch:
		branch_elem = branch.split('!=')
		return -abs(eval(branch_elem[0] + ' - (' + branch_elem[1] + ')'))
	else:
		return 0
	
def branch_look_ahead(individual):
	count = len(branches)
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	for i in branches:
		if eval(i):
			count -= 1
	return count

def fitness(individual):
	for i in range(len(individual)):
		exec("%s = %s" % (variables[i], individual[i]))
	approach_lv = len(branches) - 1
	for i in branches:
		if eval(i):
			approach_lv -= 1
		else:
			return approach_lv + normalize(branch_distance(individual, i)), branch_look_ahead(individual)
	return 0, 

# The problem is for minimizing the fitness function
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
# The individual is a list of values corresponding with 'variables' list
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attribute", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("evaluate", fitness)
toolbox.register("select", tools.selNSGA2)

def main():
	pop = toolbox.population(n=50)

	CXPB, MUTPB, NGEN = 0.5, 0.2, 50
	# Evaluate the entire population
	fitnesses = map(toolbox.evaluate, pop)
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit

	for g in range(NGEN):
		print(g)
		print(pop)
		# Select the next generation individual
		offspring = toolbox.select(pop, len(pop))
		# Clone the selected individual
		offspring = list(map(toolbox.clone, offspring))
		# Apply crossover and mutation on the offspring
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < CXPB:
				toolbox.mate(child1, child2)
				del child1.fitness.values
				del child2.fitness.values
		for mutant in offspring:
			if random.random() < MUTPB:
				toolbox.mutate(mutant)
				del mutant.fitness.values
		# Evaluate the individual with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit
		# The population is entirely replaced by the offspring
		pop[:] = offspring
	
	print(pop)
	return pop

main()
