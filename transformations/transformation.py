from node import *
from diected_acyclic_graph import *
from math import cos, sin, log

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
        Graph.add(self)
    
    '''
    Transformations have a forward and reverse method.
    These lay out the rules for the Transformation in question during either the foward or
    backward pass.
    '''
    def forward(self):
        pass
    
    def reverse(self):
        pass