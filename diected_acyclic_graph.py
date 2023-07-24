class Graph:
    '''
    This is the definition of the graph that holds all the nodes.
    The order by which Nodes are added affects the order in which calculations are done.
    As such, using appropriate parentheses is crucial in the context of this system.
    '''
    def __init__(self) -> None:
        self.nodes = []
        # Global graph object so that variables can be easily added to the graph upon declaration
        global graph 
        graph = self
    
    def add(obj):
        graph.nodes.append(obj)
    
    def get_graph():
        return graph