import random
from deap import base, creator, tools

# Now hardcoded, but later it will be replaced with data from the outside
variables = ['x', 'y', 'z']
# Now hardcoded, but later it will be replaced with data from the outside
branches = ['x + y + 2*z > 6', 'x < 10', 'y > 3', 'z < 1', 'x + y + z < 9']

IND_SIZE = len(variables)

class Toolbox:
	def __init__(self, objectives_no):
		# The problem is for minimizing the fitness function
		creator.create("FitnessMin", base.Fitness, weights=[-1.0]*objectives_no )
		# The individual is a list of values corresponding with 'variables' list
		creator.create("Individual", list, fitness=creator.FitnessMin)

		self.toolbox = base.Toolbox()
		self.toolbox.register("attribute", random.random)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attribute, n=IND_SIZE)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
		self.toolbox.register("mate", tools.cxTwoPoints)
		self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)

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

def run_ga(toolbox_object):

	pop = toolbox_object.toolbox.population(n=200)
	CXPB, MUTPB, NGEN = 0.5, 0.2, 50
	# Evaluate the entire population
	fitnesses = map(toolbox_object.toolbox.evaluate, pop)
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit

	for g in range(NGEN):
		print(g)
		print(pop)
		# Select the next generation individual
		offspring = toolbox_object.toolbox.select(pop, len(pop))
		# Clone the selected individual
		offspring = list(map(toolbox_object.toolbox.clone, offspring))
		# Apply crossover and mutation on the offspring
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < CXPB:
				toolbox_object.toolbox.mate(child1, child2)
				del child1.fitness.values
				del child2.fitness.values
		for mutant in offspring:
			if random.random() < MUTPB:
				toolbox_object.toolbox.mutate(mutant)
				del mutant.fitness.values
		# Evaluate the individual with an invalid fitness
		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox_object.toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			print(fit)
			ind.fitness.values = fit
		# The population is entirely replaced by the offspring
		pop[:] = offspring
	
	return pop

