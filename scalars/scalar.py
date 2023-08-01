from node import *
from diected_acyclic_graph import *

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
        Graph.add(self)
    
    def __repr__(self) -> str:
        return str(self.id) + "=" + str(self.value) 