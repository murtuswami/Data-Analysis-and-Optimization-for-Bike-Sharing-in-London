import pyomo


class MinCostFlow:
    """
    nodes are a list of nodes 
    edges are a 2d list of edges
    net is the flow 
    costs is the cost of sending flow along each edge,same index as edges
    capacity is the maximum amount of flow to send along each edge 
    """
    def __init__(self,nodes,edges,costs,net):
        self.nodes = nodes
        self.edges = edges
        self.costs = costs
        self.capacity = capacity

    
    def makeModel():
        return 

    def solve():
        return 