from .transformation import *

class Add(Transformation):
    '''
    Defines how two input Nodes are added together and the method by which a gradient is calculated
    '''
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