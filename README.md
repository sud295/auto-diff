# Reverse Auto Differentiation

## Summary
Given a function, this program will create a Directed Acyclic Graph of that function and return the partial derivatives with respect to every variable as well as the output of the function at specified values of the variables. This program utilizes reverse-mode auto-differentiation where gradients are calculated during the backward pass of the graph, similar to popular frameworks like TensorFlow. See arXiv:1502.05767.

## Instructions
First, create a Python project in the same directory as "auto_diff.py" and import auti_diff.
```
from auto_diff import *
```
Create an instance of a graph.
```
Graph()
```
Define any variables and constants. Pass in the value at which the variable is to be evaluated as well as a name if desired (name will be auto-generated otherwise)
```
v_0 = Variable(2,'x')
v_1 = Variable(5,'y')
v_2 = Constant(9)
```
Define the function. For adding, subtracting, multiplying, dividing and raising to a power, it is possible to use "+","-","*","/","**".
```
v_3 = Log(v_0) + v_0*v_1 - Sin(v_1) + v_2
```
Run the forward pass. This will output the result of the function at the specified values.
```
print("Forward Pass = ",forward_pass())
```
Run the backward pass. This will calculate all the gradients.
```
backward_pass()
```
Now that all the partials have been calculated, we just need to obtain those of the variables. Use the "get_partials()" method for this.
```
print(get_partials())
```
