from .transformation import *

class Cos(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Cos", id=id)

    def forward(self):
        return cos(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return [sin(self.inputs[0].value) * (-1 * cotangent_information)]