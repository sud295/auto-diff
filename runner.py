from auto_diff import *

def main():
    dag = Graph()
    v_0 = Variable(5,'x')
    v_1 = Variable(6,'y')
    v_2 = Variable(7,'z')
    v_3 = v_0 * (Sin(v_1) + Cos(v_2))
    print("Forward Pass = ",forward_pass())
    backward_pass()
    for node in dag.nodes:
        if isinstance(node, Variable):
            print(f"d/d{node.id} = ", node.gradient)

if __name__ == "__main__":
    main()