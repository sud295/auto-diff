from .scalar import *

class Variable(Scalar):
    '''
    The goal of this program is to see how Variables affect the output of the function
    '''
    def __init__(self, value, id = None) -> None:
        super().__init__(value=value, type="Variable", id=id)