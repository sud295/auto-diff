from auto_diff import *

# Example of how to use the module
def main():
    a = Graph()

    v_0 = Variable(-1,'x')
    # v_1 = Variable(5,'y')
    # v_2 = Log(v_0) + v_0*v_1 - Sin(v_1)
    v_2 = v_0**Constant(2)

    print("Forward Pass = ",forward_pass())
    backward_pass()
    
    partials = get_partials()
    partials = [partial[1] for partial in partials]
    print(partials)
    print(a.nodes)

if __name__ == "__main__":
    main()