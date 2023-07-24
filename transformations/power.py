from .transformation import *

class Power(Transformation):
    def __init__(self, a, b, id = None) -> None:
        super().__init__(a=a,b=b,type="Power", id=id)
    
    def forward(self):
        return self.inputs[0].value ** self.inputs[1].value
    
    def reverse(self, adjoint):
        return adjoint * self.inputs[1].value * (self.inputs[0].value ** (self.inputs[1].value - 1)), adjoint * log(self.inputs[0].value) * (self.inputs[0].value ** self.inputs[1].value)
    