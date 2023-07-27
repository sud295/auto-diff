from auto_diff import *

# Example of how to use the module
def main():
    Graph()

    v_0 = Variable(2,'x')
    v_1 = Variable(5,'y')
    v_2 = Log(v_0) + v_0*v_1 - Sin(v_1)

    print("Forward Pass = ",forward_pass())
    backward_pass()

    print(get_partials())

if __name__ == "__main__":
    main()