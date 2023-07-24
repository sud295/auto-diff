from .transformation import *

class Subtract(Transformation):
    '''
    Defines how two input Nodes are subtracted and the method by which a gradient is calculated
    '''
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Subtract", id=id)
    
    def forward(self):
        return self.inputs[0].value - self.inputs[1].value
    
    def reverse(self, cotangent_information):
        return cotangent_information, -1 * cotangent_information 
