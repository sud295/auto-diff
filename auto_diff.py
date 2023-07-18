from math import sin, cos, log

class Node():
    '''
    Placeholder Node class for overriding operators like "+", "-", etc.
    '''
    pass

class Scalar(Node):
    '''
    Class that represents a Scalar which, in this context, is just some number that can either be
    a variable or a constant
    '''
    identifier = 0
    def __init__(self, value, type, id = None) -> None:
        self.value = value
        self.gradient = None
        if id == None:
            self.id = f"{type}: " + str(Scalar.identifier + 1)
        else:
            self.id = id
        Scalar.identifier += 1

        # Add each new Scalar to the directed acyclic graph
        graph.nodes.append(self)
    
class Transformation(Node):
    '''
    A Transformation is the second type of Node. 
    It represents operations on scalars and other Transformation nodes.
    As such, Transformations have inputs that are used to perform some computation.
    '''
    identifier = 0
    def __init__(self, a, b, type, id = None) -> None:
        self.inputs = [a,b]
        self.value = None
        self.gradient = None
        if id == None:
            self.id = f"{type}: " + str(Transformation.identifier + 1)
        else:
            self.id = id
        Transformation.identifier += 1

        # Add each new Transformation to the directed acyclic graph
        graph.nodes.append(self)
    
    '''
    Transformations have a forward and reverse method.
    These lay out the rules for the Transformation in question during either the foward or
    backward pass.
    '''
    def forward(self):
        pass
    
    def reverse(self):
        pass

'''
At the end of the day, we want to see how Variables affect the output of the function
'''
class Variable(Scalar):
    def __init__(self, value, id = None) -> None:
        super().__init__(value=value, type="Variable", id=id)

'''
Constants are just factors that either shift or scale the function
'''
class Constant(Scalar):
    def __init__(self, value, id = None) -> None:
        super().__init__(value=value, type="Constant", id=id)

'''
Defines how two input Nodes are added together and the method by which a gradient is calculated
'''
class Add(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Add", id=id)
    
    def forward(self):
        return self.inputs[0].value + self.inputs[1].value
    
    '''
    The derivative of a variable is 1
    See README for more about "cotangent_information"
    '''
    def reverse(self, cotangent_information):
        return cotangent_information, cotangent_information 

'''
Defines how two input Nodes are multiplied together and the method by which a gradient is calculated
'''
class Multiply(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Multiply", id=id)
    
    def forward(self):
        return self.inputs[0].value * self.inputs[1].value
    
    '''
    While taking partial derivatives, we treat the other Node as a constant, hence we return the value of just the other Node
    along with some gradient information from following nodes in the graph (cotangent_information)
    '''
    def reverse(self, cotangent_information):
        return self.inputs[1].value * cotangent_information, self.inputs[0].value * cotangent_information

'''
Defines how two input Nodes are subtracted and the method by which a gradient is calculated
'''
class Subtract(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Subtract", id=id)
    
    def forward(self):
        return self.inputs[0].value - self.inputs[1].value
    
    def reverse(self, cotangent_information):
        return cotangent_information, -1 * cotangent_information 

'''
Defines how two input Nodes are divided and the method by which a gradient is calculated
'''
class Divide(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Divide", id=id)

    def forward(self):
        return self.inputs[0].value / self.inputs[1].value
    
    # Use the quotient rule with respect to each input a and b
    def reverse(self, cotangent_information):
        return cotangent_information/self.inputs[1].value, cotangent_information*self.inputs[0].value/(self.inputs[1].value ** 2)

class Sin(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Sin", id=id)

    def forward(self):
        return sin(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return [cos(self.inputs[0].value) * cotangent_information]

class Cos(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Sin", id=id)

    def forward(self):
        return cos(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return [sin(self.inputs[0].value) * (-1 * cotangent_information)]

class Log(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Log", id=id)
    
    def forward(self):
        return log(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return [cotangent_information/self.inputs[0].value]
    
'''
This is the definition of the graph that holds all the nodes.
The order by which Nodes are added affects the order in which calculations are done.
As such, using appropriate parentheses is crucial in the context of this system.
'''
class Graph:
    def __init__(self) -> None:
        self.nodes = []
        # Global graph object so that variables can be easily added to the graph upon declaration
        global graph 
        graph = self

'''
The forward pass simply calculates the value at each node and ultimately the output of the function
'''
def forward_pass():
    for node in graph.nodes:
        if isinstance(node, Transformation):
            node.value = node.forward()
    # Returns the output of the function (value of the last node)
    return graph.nodes[-1].value

'''
The backward pass calculates the gradient at each node, starting from the last node.
The adjoint operator is especially important in the backward pass:
    More information on this in the README

'''
def backward_pass():
    # Keep track of nodes visited
    visited_nodes = set()

    # Since our gradients are with respect to the output of the function, the gradient of the last node is 1 (wrt itself)
    graph.nodes[-1].gradient = 1
    for node in reversed(graph.nodes):
        if isinstance(node, Transformation):
            # Obtain the inputs so that we can traverse through them
            input_nodes = node.inputs
            # Returns all the gradients with respect to each input
            gradients = node.reverse(node.gradient)
            # Pair each input with its coresponding gradient
            groups = zip(input_nodes, gradients)
            for input_node, node_gradient in groups:
                if input_node not in visited_nodes:
                    input_node.gradient = node_gradient
                else:
                    input_node.gradient += node_gradient
                visited_nodes.add(input_node)
    gradient_tape = []
    for node in graph.nodes:
        gradient_tape.append(node.gradient)
    return gradient_tape

'''
Link the default '+,-,*,/' operations with their corresponding Classes
'''
def node_add(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Add(self, other)

def node_mul(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Multiply(self, other)

def node_sub(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Subtract(self, other)

def node_div(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Divide(self, other)

Node.__add__ = node_add
Node.__mul__ = node_mul
Node.__sub__ = node_sub
Node.__div__ = node_div