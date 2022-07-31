import pyomo
import pandas
import pyomo.opt
import pyomo.environ as pyo



class MinCostFlow:
    """
    nodes is a dataframe containing id as index and imbalance as column 
    edges are a dataframe containing [start,end] as index with weights and capacities
    Code was adapted from the following : 


    https://github.com/Pyomo/PyomoGallery/blob/master/pandas_min_cost_flow/min_cost_flow.py
    """
    def __init__(self,nodesDF,edgesDF):
        self.edges_data = edgesDF
        self.node_data = nodesDF
        self.node_set = nodesDF.index.unique()
        self.edge_set = edgesDF.index.unique()
    
    def makeModel(self):
        self.m = pyo.ConcreteModel()

        self.m.node_set = pyo.Set(initialize = self.node_set)
        self.m.edge_set = pyo.Set(initialize = self.edge_set,dimen = 2 )
        #Make rule that we cant send flow along an edge unless its X value is true 

        self.m.X = pyo.Var(self.m.edge_set,domain=pyo.NonNegativeReals) 
        self.m.Y = pyo.Var(self.m.edge_set,within = Binary )

        #Objective rule 
        def obj_rule(m):
            return sum(m.Y[e] * self.edges_data.ix[e,'weight'] for e in self.edge_set) 
        self.m.Obj = pyo.Objective(rule = obj_rule,sense = pyo.minimize)

        #Flow Conservation 
        def flow_conservation(m,n): # m is model, n is node id that we are conserving flow 
            edges = self.edges_data.reset_index()
            incoming = edges[edges.edgeEnd ==n ]['edgeStart']
            outgoing = edges[edges.edgeStart == n]['edgeEnd']
            return sum(m.X[(p,n)] for p in incoming) - sum(m.Y[(n,s)] for s in outgoing ) == self.node_data.ix[n,'imbalance']
        self.m.FlowCons = pyo.Constraint(self.m.node_set,rule = flow_conservation)

        def flow_along_active_edge(m,n):
            # flow, X must be greater than or equal to than Y which decides whether the edge is active 
            # lets say edge is not active, so Y = 0. We sent 1 unit of flow, so it wont work 
            # lets say edge is active. Y = 1. minimum flow is 1. So  X>=Y it will send 
            return self.m.X[n] >= self.m.Y[n]
        self.m.activeEdges = pyo.Constraint(self.m.edge_set,rule=flow_along_active_edge)

    def solve(self):
        return 