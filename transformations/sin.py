from .transformation import *

class Sin(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Sin", id=id)

    def forward(self):
        return sin(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return [cos(self.inputs[0].value) * cotangent_information]
