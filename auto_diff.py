from math import sin, cos

class Node():
    pass

class Scalar(Node):
    identifier = 0
    def __init__(self, value, type, id = None) -> None:
        self.value = value
        self.gradient = None
        if id == None:
            self.id = f"{type}: " + str(Scalar.identifier + 1)
        else:
            self.id = id
        Scalar.identifier += 1
        graph.nodes.append(self)
    
class Transformation(Node):
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
        graph.nodes.append(self)
    
    def forward(self):
        pass
    
    def reverse(self):
        pass

class Variable(Scalar):
    def __init__(self, value, id = None) -> None:
        super().__init__(value=value, type="Variable", id=id)

class Constant(Scalar):
    def __init__(self, value, id = None) -> None:
        super().__init__(value=value, type="Constant", id=id)
    
class Add(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Add", id=id)
    
    def forward(self):
        return self.inputs[0].value + self.inputs[1].value
    
    def reverse(self, cotangent_information):
        return cotangent_information, cotangent_information 

class Multiply(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Multiply", id=id)
    
    def forward(self):
        return self.inputs[0].value * self.inputs[1].value
    
    def reverse(self, cotangent_information):
        return self.inputs[1].value * cotangent_information, self.inputs[0].value * cotangent_information

class Subtract(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Subtract", id=id)
    
    def forward(self):
        return self.inputs[0].value - self.inputs[1].value
    
    def reverse(self, cotangent_information):
        return cotangent_information, -1 * cotangent_information 

class Divide(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Divide", id=id)

    def forward(self):
        return self.inputs[0].value / self.inputs[1].value
    
    def reverse(self, cotangent_information):
        return cotangent_information/self.inputs[1].value, cotangent_information*self.inputs[0].value/(self.inputs[1].value ** 2)

class Sin(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Sin", id=id)

    def forward(self):
        return sin(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return cotangent_information * cos(self.inputs[0].value)

class Cos(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Sin", id=id)

    def forward(self):
        return cos(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return -1 * cotangent_information * sin(self.inputs[0].value)

class Graph:
    def __init__(self) -> None:
        self.nodes = []
        global graph 
        graph = self

def forward_pass():
    for node in graph.nodes:
        if isinstance(node, Transformation):
            node.value = node.forward()
    return graph.nodes[-1].value

def backward_pass():
    visited_nodes = set()
    graph.nodes[-1].gradient = 1
    for node in reversed(graph.nodes):
        if isinstance(node, Transformation):
            input_nodes = node.inputs
            gradients = node.reverse(node.gradient)
            for input_node, node_gradient in zip(input_nodes, gradients):
                if input_node not in visited_nodes:
                    input_node.gradient = node_gradient
                else:
                    input_node.gradient += node_gradient
                visited_nodes.add(input_node)
    gradient_tape = []
    for node in graph.nodes:
        gradient_tape.append(node.gradient)
    return gradient_tape

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

def node_sin(self):
    return Sin(self)

def node_cos(self):
    return Cos(self)

Node.__add__ = node_add
Node.__mul__ = node_mul
Node.__sub__ = node_sub
Node.__div__ = node_div
Node.sin = node_sin
Node.cos = node_cos