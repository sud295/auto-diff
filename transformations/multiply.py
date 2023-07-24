from .transformation import *

class Multiply(Transformation):
    '''
    Defines how two input Nodes are multiplied together and the method by which a gradient is calculated
    '''
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
