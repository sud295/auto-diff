class Node():
    pass

class Scalar(Node):
    identifier = 0
    def __init__(self, value, type, id = None) -> None:
        self.value = value
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
    
    def gradient(self):
        return 0

class Add(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Add", id=id)
    
    def forward(self):
        return self.inputs[0].value + self.inputs[1].value
    
    def reverse(self):
        pass

class Multiply(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Multiply", id=id)
    
    def forward(self):
        return self.inputs[0].value * self.inputs[1].value
    
    def reverse(self):
        pass

class Subtract(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Subtract", id=id)
    
    def forward(self):
        return self.inputs[0].value - self.inputs[1].value
    
    def reverse(self):
        pass

class Divide(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Divide", id=id)

    def forward(self):
        return self.inputs[0].value / self.inputs[1].value
    
    def reverse(self):
        pass

class Graph:
    def __init__(self) -> None:
        self.nodes = []
        global graph 
        graph = self
    
    def __enter__(self):
        return self
    
    def __exit__(sel, exc_type, exc_value, tracebackf) -> None:
        try:
            del self
        except:
            pass

def forward_pass():
    for node in graph.nodes:
        if isinstance(node, Transformation):
            node.value = node.forward()
    return graph.nodes[-1].value

def node_add(self, other):
    if not isinstance(other, Node):
        raise Exception("Incompatible Argument")
    return Add(self, other)

def node_mul(self, other):
    if not isinstance(other, Node):
        raise Exception("Incompatible Argument")
    return Multiply(self, other)

def node_sub(self, other):
    if not isinstance(other, Node):
        raise Exception("Incompatible Argument")
    return Subtract(self, other)

def node_div(self, other):
    if not isinstance(other, Node):
        raise Exception("Incompatible Argument")
    return Divide(self, other)

Node.__add__ = node_add
Node.__mul__ = node_mul
Node.__sub__ = node_sub
Node.__div__ = node_div

with Graph() as dag:
    v_0 = Variable(5)
    v_1 = Variable(6)
    v_2 = (v_0+v_1) * v_0
    print(forward_pass())