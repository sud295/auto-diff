from node import *
from transformations.types import *

'''
Link the default '+,-,*,/' operations with their corresponding Classes
'''

def node_add(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Add(self, other)

def node_mul(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Multiply(self, other)

def node_sub(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Subtract(self, other)

def node_div(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Divide(self, other)

def node_pow(self, other):
    if not isinstance(other, Node):
        raise Exception(f"Incompatible Argument \"{other}\"")
    return Power(self, other)

Node.__add__ = node_add
Node.__mul__ = node_mul
Node.__sub__ = node_sub
Node.__truediv__ = node_div
Node.__pow__ = node_pow