from .transformation import *

class Divide(Transformation):
    '''
    Defines how two input Nodes are divided and the method by which a gradient is calculated
    '''
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Divide", id=id)

    def forward(self):
        return self.inputs[0].value / self.inputs[1].value
    
    # Use the quotient rule with respect to each input a and b
    def reverse(self, cotangent_information):
        return cotangent_information/self.inputs[1].value, -1 * cotangent_information*self.inputs[0].value/(self.inputs[1].value ** 2)
