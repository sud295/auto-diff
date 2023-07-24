from .scalar import *

class Constant(Scalar):
    '''
    Constants are just factors that either shift or scale the function
    '''
    def __init__(self, value, id = None) -> None:
        super().__init__(value=value, type="Constant", id=id)