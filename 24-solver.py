import itertools
import math

SHOW_ANSWERS = False

INF = 10000

class Type:
    Operation = 1
    Number = 2

class Operation:
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    
class Node:
    def __init__(self, type):
        self.type = type
        self.negatives = False;
    
    def set_num(self, number):
        if (self.type == Type.Operation):
            print("Expected operation")
        self.number = number
    
    def set_op(self, operation):
        if (self.type == Type.Number):
            print("Expected number")
        self.operation = operation;
        
    def set_children(self, left, right):
        self.left = left
        self.right = right
        
    def get_num(self):
        return self.number
    
    def get_op(self):
        return self.operation
    
    def has_negatives(self):
        if self.type == Type.Number:
            return self.get_num() < 0
        return self.eval() < 0 or self.left.has_negatives() or self.right.has_negatives() < 0
    
    def flatten(self):
        pass
    
    def arrange(self):
        pass
    
    def eval(self):
        if self.type == Type.Number:
            return self.get_num()
        elif self.operation == Operation.ADD:
            return self.left.eval() + self.right.eval()
        elif self.operation == Operation.SUB:
            return self.left.eval() - self.right.eval()
        elif self.operation == Operation.MUL:
            return self.left.eval() * self.right.eval()
        elif self.operation == Operation.DIV:
            if (self.right.eval() == 0):
                return INF
            return self.left.eval() / self.right.eval()
        
    def __str__(self):
        if self.type == Type.Number:
            return str(self.get_num())
        else:
            return '(' + str(self.left) + ' ' + self.operation + ' ' + str(self.right) + ')'
        
        
class UNode:
    def __init__(self, type):
        self.type = type
        self.negatives = False;
        self.exprs = []
    
    def set_num(self, number):
        if (self.type == Type.Operation):
            print("Expected operation")
        self.number = number
    
    def set_op(self, operation):
        if (self.type == Type.Number):
            print("Expected number")
        self.operation = operation;
        
    def set_children(self, left, right):
        self.left = left
        self.right = right
        
    def get_num(self):
        return self.number
    
    def get_op(self):
        return self.operation
    
    def has_negatives(self):
        if self.type == Type.Number:
            return self.get_num() < 0
        return self.eval() < 0 or self.left.has_negatives() or self.right.has_negatives()
    
    def flatten(self):
        if self.type == Type.Number:
            self.exprs = [self]
            return
        
        self.left.flatten()
        self.right.flatten()

        if self.operation == Operation.ADD or self.operation == Operation.MUL:
            if self.left.type == Type.Number:
                self.exprs = self.left.exprs
            elif self.left.operation == self.operation:
                self.exprs = self.left.exprs
            else:
                self.exprs = [self.left]
                
            if self.right.type == Type.Number:
                self.exprs = self.exprs + self.right.exprs
            elif self.right.operation == self.operation:
                self.exprs = self.exprs + self.right.exprs
            else:
                self.exprs = self.exprs + [self.right]
            return self.exprs
        
        else:
            if self.left.type == Type.Number:
                self.exprs = [self.left, self.right]
            elif self.left.operation == self.operation:
                self.exprs = self.left.exprs + [self.right]
            else:
                self.exprs = [self.left, self.right]
        
    def arrange(self):
        if self.type == Type.Operation:
            if (self.operation == Operation.ADD or self.operation == Operation.MUL):
                self.exprs = sorted(self.exprs, key = lambda x : x.eval()) 
            else:
                self.exprs = [self.exprs[0]] + sorted(self.exprs[1:], key = lambda x : x.eval())
            
            for expr in self.exprs:
                expr.arrange()
                
    def eval(self):
        if self.type == Type.Number:
            return self.get_num()
        elif self.operation == Operation.ADD:
            return sum([expr.eval() for expr in self.exprs])
        elif self.operation == Operation.SUB:
            return self.exprs[0].eval() - sum([expr.eval() for expr in self.exprs[1:]])
        elif self.operation == Operation.MUL:
            cur = 1
            for x in self.exprs:
                cur *= x.eval()
            return cur
        elif self.operation == Operation.DIV:
            cur = self.exprs[0].eval()
            for x in self.exprs[1:]:
                if (x.eval() == 0):
                    return INF
                cur /= x.eval()
            return cur
        
    def __str__(self):
        if self.type == Type.Number:
            return str(self.get_num())
        else:
            return '(' + (" " + self.operation + " ").join([str(expr) for expr in self.exprs]) + ')'
        
        
structures = [
    [
        Type.Operation,
        [
            Type.Operation,
            [
                Type.Operation,
                Type.Number,
                Type.Number
            ],
            Type.Number
        ],
        Type.Number
    ],
    
    [
        Type.Operation,
        [
            Type.Operation,
            Type.Number,
            [
                Type.Operation,
                Type.Number,
                Type.Number
            ]
        ],
        Type.Number
    ],
    
    [
        Type.Operation,
        [
            Type.Operation,
            Type.Number,
            Type.Number
        ],
        [
            Type.Operation,
            Type.Number,
            Type.Number
        ]
    ],
    
    [
        Type.Operation,
        Type.Number,
        [
            Type.Operation,
            [
                Type.Operation,
                Type.Number,
                Type.Number
            ],
            Type.Number
        ]
    ],
    
    [
        Type.Operation,
        Type.Number,
        [
            Type.Operation,
            Type.Number,
            [
                Type.Operation,
                Type.Number,
                Type.Number
            ]
        ]
    ]
]

def generate_tree(structure, op_list, num_list, dupes):
    NodeClass = Node if dupes else UNode
    if structure == Type.Number:
        node = NodeClass(Type.Number)
        node.set_num(num_list.pop())
        return node
    elif structure[0] == Type.Operation:
        node = NodeClass(Type.Operation)
        node.set_op(op_list.pop())
        left = generate_tree(structure[1], op_list, num_list, dupes)
        right = generate_tree(structure[2], op_list, num_list, dupes)
        node.set_children(left, right)
        return node
        
ops = [Operation.ADD, Operation.SUB, Operation.MUL, Operation.DIV]
num_list = [1,2,3,4]

def solve(nums, dupes=False, negatives=False):
    solutions = []
    for structure in structures:
        for perm in list(itertools.permutations(nums)):
            for x in ops:
                for y in ops:
                    for z in ops:
                        cur = generate_tree(structure, [x,y,z], list(perm), dupes)
                        cur.flatten()
                        cur.arrange()
                        if (round(cur.eval(), 2) == 24 and (negatives or not cur.has_negatives())):
                            solutions.append(cur)
                            
    return solutions

solutions = solve([1,5,6,4], False, False)
solution_strings = list(set([str(sol) for sol in solutions]))
    

if SHOW_ANSWERS:
    for sol in solution_strings:
        print(sol[1:-1])
else:
    print(len(solution_strings) > 0)


