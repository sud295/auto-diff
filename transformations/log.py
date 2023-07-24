from .transformation import *

class Log(Transformation):
    def __init__(self, a, id = None) -> None:
        super().__init__(a=a,b=None, type="Log", id=id)
    
    def forward(self):
        return log(self.inputs[0].value)
    
    def reverse(self, cotangent_information):
        return [cotangent_information/self.inputs[0].value]