from auto_diff import *

def main():
    Graph()
    v_0 = Variable(5,'x')
    v_1 = Variable(6,'y')
    v_2 = (v_0-v_1) * v_0
    print(forward_pass())
    backward_pass()
    print(v_0.gradient)
    print(v_1.gradient)

if __name__ == "__main__":
    main()