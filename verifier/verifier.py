import sys, os
import shutil
import re
import operator
class InvalidException(Exception):
	def __init__(self, msg):
		self.msg = msg

class Node(object):
	def __init__(self, l_number):
		self.l_number = l_number
		self.edge = []

	def push_edge(self, condition, next_line, negation = False):
		self.edge.append((condition, next_line, negation))
	
class Pattern:
    ptn_declare = re.compile('(int .*;|byte .*;)')
    ptn_label = re.compile('^label[0-9]+:$')
    ptn_branch = re.compile('if .* goto')
    ptn_throw = re.compile('throw .*')
    ptn_testme = re.compile('public void testMe\(int(, int)*\)') # entry point of program
    ptn_goto = re.compile('^goto .*')
    ptn_expression = re.compile('[\$A-Za-z_][\$A-Za-z0-9_]+ = .*')
    ptn_param = re.compile('@parameter[0-9]+: int;')
    ptn_signature = re.compile('.*invoke.*signature')

class ShimpleInstance(object):

    def __init__(self, path):
        self.path = path
        self.generate_shimple()
        self.variables = {}
        self.params = []
        self.labels = {}
        self.gotos_and_branches = []
        self.flow_graph = {}
        self.validity = True
        self.root = None
        self.sorted_labes = []
        self.path = []
    
    def set_path(self, path):
        self.path = path

    def generate_shimple(self):
        if self.path.find('.java') == -1:
            raise
        self.file_name = self.path.split('/')[-1].split('.java')[0]
        shutil.copyfile(self.path, 'soot/' + self.file_name + '.java')
        os.chdir('soot/')
        os.system('javac ' + self.file_name + '.java')
        os.system('./soot.sh ' + self.file_name)

    def cleanup_shimple(self):
        # os.remove('./%s.java' % self.file_name)
        # os.remove('./%s.class' % self.file_name)
        # os.remove('./%s.shimple' % self.file_name)
        os.chdir('../')
        pass

    def declare_param(self, x):
        self.params.append(x)
    
    def declare_variable(self, name, expr):
        for i in self.variables:
            expr = expr.replace(i, self.variables[i])
        self.variables[name] = expr

    def declare_token(self, x):
        self.variables[x] = Int(x)

    def add_expression(self, expr, phi = None, negation = False):
        if 'Phi' in expr:
            phi_dict = {}
            phi_index = expr.find('Phi(')
            phi_values = expr.split('Phi(')[1][:-1].split(', ')
            for values in phi_values:
                sp_values = values.split(' #')
                if sp_values[1] == str(phi):
                    expr = expr[:phi_index] + sp_values[0]
                    break
        def __wrap_variables(match):
            return 'self.variables[\'%s\']' % match.group(0)
        sub_expr = re.sub(r'[\$A-Za-z_][\$A-Za-z0-9_]+', __wrap_variables, expr)
        if negation:
            sub_expr = 'Not(' + sub_expr + ')'
        sub_expr = 'self.solver.add(' + sub_expr + ')'
        try:
            eval(sub_expr)
        except:
            # print 'Error: ' + sub_expr
            return False | negation
        return True

    def interpret(self):
        self.solver = Solver()
        def __dfs__(node, phi = None):
            line = self.code[node.l_number]
            next_phi = None
            match_phi = re.match(r'\([0-9]+\)', line)
            if match_phi:
                raw_phi = match_phi.group(0)
                next_phi = int(raw_phi[1:-1])
                line = line[len(raw_phi):].strip()
                # print 'next phi is ' + str(next_phi)
            # print '(%d) %s' % (node.l_number + 1, line)
            if Pattern.ptn_declare.search(line):
                tokens = None
                if line[:3] == 'int':
                    tokens = line[4:-1].split(', ')
                else:
                    tokens = line[5:-1].split(', ')
                for x in tokens:
                    self.declare_token(x)
            elif Pattern.ptn_param.search(line):
                self.declare_param(line.split(':=')[0].strip())
            elif Pattern.ptn_expression.search(line):
                self.add_expression(line.replace('=', '==')[:-1], phi)
            elif Pattern.ptn_throw.search(line):
                if self.solver.check() == sat:
                    model = self.solver.model()
                    t_model = []
                    for param in self.params:
                        t_model.append(model.evaluate(self.variables[param]))
                    # print model
                    self.cleanup_shimple()
                    raise InvalidException(t_model)
            elif phi and not next_phi:
                next_phi = phi
            for edge in node.edge:
                if edge[0]:
                    self.solver.push()
                    if self.add_expression(edge[0], phi, edge[2]):
                        __dfs__(self.flow_graph[edge[1]], next_phi)
                    self.solver.pop()
                else:
                    __dfs__(self.flow_graph[edge[1]], next_phi)
        __dfs__(self.root)

    def get_labels(self):
        test_me = 0
        for number, line in enumerate(self.code):
            number = number+1
            if not test_me:
                if Pattern.ptn_testme.search(line):
                    test_me = 1
            else:
                if line == '}':
                    break
                elif Pattern.ptn_label.search(line):
                    self.labels[line[:-1]] = number
                elif Pattern.ptn_expression.search(line):
                    name_expr = line.split('=')
                    name = name_expr[0].strip()
                    expr = name_expr[1].split(';')[0]
                    self.declare_variable(name, expr)
                elif Pattern.ptn_param.search(line):
                    self.declare_param(line.split(':=')[0].strip())
                elif Pattern.ptn_goto.search(line) or Pattern.ptn_branch.search(line):
                    self.gotos_and_branches.append(number)
                elif Pattern.ptn_signature.search(line):
                    self.signature = number

    def find_all_jump(self):
        test_me = 0
        for number, line in enumerate(self.code):
            number = number+1
            if not test_me:
                if Pattern.ptn_testme.search(line):
                    test_me = 1
            else:
                if line == '}':
                    break
                elif Pattern.ptn_goto.search(line) or Pattern.ptn_branch.search(line):
                    self.gotos_and_branches.append(number)
            if Pattern.ptn_signature.search(line):
                self.signature = number

    def find_next_line_number(self, number):
        for n in self.gotos_and_branches:
            if n > number:
                return n


    def construct_graph(self):
        test_me = 0
        for number, line in enumerate(self.code):
            number = number+1
            if not test_me:
                if Pattern.ptn_testme.search(line):
                    test_me = 1
            elif test_me == 1:
                if not self.root:
                    self.root = Node(number)
                    current_node = self.root
                else:
                    current_node = Node(number)
                match_phi = re.match(r'\([0-9]+\)', line)
                if match_phi:
                    raw_phi = match_phi.group(0)
                    line = line[len(raw_phi):].strip()
                if line == '}':
                    break
                elif Pattern.ptn_branch.search(line):
                    condition = line.split('if')[1].split('goto')[0].strip()
                    l_number = self.find_next_line_number(self.labels[line.split('goto')[1][:-1].strip()])
                    current_node.push_edge(condition, l_number)
                    next_line_number = self.find_next_line_number(number)
                    current_node.push_edge(condition, next_line_number, True)
                    self.flow_graph[number] = current_node
                elif Pattern.ptn_goto.search(line):
                    l_number = self.find_next_line_number(self.labels[line[5:-1]])
                    current_node.push_edge('goto', l_number)
                    self.flow_graph[number] = current_node

    def scan(self):
        shimple_file = open(self.file_name + '.shimple')
        lines = shimple_file.readlines()
        self.code = [x.strip() for x in lines]
        self.get_labels()
        self.construct_graph()
        shimple_file.close()

    def find_entry_point(self):
        for i in range(self.signature-1, -1, -1):
            if Pattern.ptn_branch.search(self.code[i]) or Pattern.ptn_goto.search(self.code[i]):
                return i+1
    

    def find_path(self, number, path):
        for k, v in self.flow_graph.items():
            for edge in v.edge:
                if edge[1] == number:
                    path.append(edge)
                    return self.find_path(k, path)
        path.reverse()
        return path

    def negation_and_mapping(self, path):
        negation_map = {'=':'!=', '!=':'=', '>':'<=', '<':'>=', '>=':'<', '<=':'>'}
        real_path = []
        for condition in path:
            if not condition[2]:
                real_path.append(condition[0])
            else:
                condition_split = condition[0].split()
                condition_split[1] = negation_map[condition_split[1]]
                real_path.append(' '.join(condition_split))

        for idx, edge in enumerate(real_path):
            split_edge = edge.split() 
            if split_edge[0] in self.variables:
                split_edge[0] = self.variables[split_edge[0]].strip()
            if split_edge[2] in self.variables:
                split_edge[2] = self.variables[split_edge[2]].strip()
            real_path[idx] = " ".join(split_edge)

        return real_path

def main():
    instance = ShimpleInstance(sys.argv[1])
    instance.scan()
    # instance.interpret() # contains dfs of cfg
    instance.cleanup_shimple()
    entry_point = instance.find_entry_point()
    path = instance.find_path(entry_point, [instance.flow_graph[entry_point].edge[1]])
    instance.set_path(instance.negation_and_mapping(path))
    for idx, p in enumerate(instance.path):
        p = p.replace('cmpl', '-')
        p = p.replace('cmpg', '-')
        instance.path[idx] = p.replace('(double)', '')
    print(instance.path)

    ############ 현우는 여기 아래서  부터 instance가지고 노시면 됩니다 #############

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise
        main()
        print('VALID')
    except InvalidException as e:
        print('INVALID')
        print(e.msg)

