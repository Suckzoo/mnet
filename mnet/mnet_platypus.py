from platypus import NSGAII, Problem, Real
import sys
sys.path.append('../traditional')
from traditional import fitness

# Now hardcoded, but later it will be replaced with data from the outside
variables = ['x', 'y', 'z']
# Now hardcoded, but later it will be replaced with data from the outside
branches = ['x + y + 2*z > 6', 'x < 10', 'y > 3']

class Mnet(Problem):

	def __init__(self):
		super(Mnet, self).__init__(3, 2)
		self.types[:] = [Real(-100, 100) for i in range(len(variables))]

	def branch_look_ahead(self, individual):
		count = len(individual)
		for i in range(len(individual)):
			exec("%s = %s" % (variables[i], individual[i]))
		for i in branches:
			if eval(i):
				count -= 1
		return count

	def evaluate(self, solution):
		solution.objectives[:] = fitness(solution.variables)[0], self.branch_look_ahead(solution.variables)

algorithm = NSGAII(Mnet())
algorithm.run(10)

for solution in algorithm.result:
	print(solution.objectives)
