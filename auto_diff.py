from diected_acyclic_graph import *
from scalars.types import *
from transformations.types import *
from wrappers import *

def forward_pass():
    '''
    The forward pass simply calculates the value at each node and ultimately the output of the function
    '''
    for node in Graph.get_graph().nodes:
        if isinstance(node, Transformation):
            node.value = node.forward()
    # Returns the output of the function (value of the last node)
    return Graph.get_graph().nodes[-1].value

def backward_pass():
    '''
    The backward pass calculates the gradient at each node, starting from the last node.
    The adjoint operator is especially important in the backward pass:
        More information on this in the README
    '''

    # Keep track of nodes visited
    visited_nodes = set()

    # Since our gradients are with respect to the output of the function, the gradient of the last node is 1 (wrt itself)
    Graph.get_graph().nodes[-1].gradient = 1
    for node in reversed(Graph.get_graph().nodes):
        if isinstance(node, Transformation):
            # Obtain the inputs so that we can traverse through them
            input_nodes = node.inputs
            # Returns all the gradients with respect to each input
            gradients = node.reverse(node.gradient)
            # Pair each input with its coresponding gradient
            groups = zip(input_nodes, gradients)
            for input_node, node_gradient in groups:
                if input_node not in visited_nodes:
                    input_node.gradient = node_gradient
                else:
                    input_node.gradient += node_gradient
                visited_nodes.add(input_node)
    gradient_tape = []
    for node in Graph.get_graph().nodes:
        gradient_tape.append(node.gradient)
    return gradient_tape

def get_partials():
    '''
    Returns a list of all the partial derivatives of the input function
    '''
    partials = []
    for node in Graph.get_graph().nodes:
        if isinstance(node, Variable):
            inner_list = []
            inner_list.append(f"d/d{node.id}")
            inner_list.append(node.gradient)
            partials.append(inner_list)
    return partials