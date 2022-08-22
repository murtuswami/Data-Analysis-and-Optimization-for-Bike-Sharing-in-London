import pyomo
import pandas
import pyomo.opt
import pyomo.environ as pyo
import pdb
from pyomo.environ import value


class MinCostFlow:
    """
    nodes is a dataframe containing id as index and imbalance as column 
    edges are a dataframe containing [start,end] as index with weights and capacities
    """
    def __init__(self,nodesDF,edgesDF):
        self.edge_data = edgesDF
        self.node_data = nodesDF
        self.node_set = nodesDF.index.unique()
        self.edge_set = edgesDF.index.unique()
    
    def makeModel(self):
        self.m = pyo.ConcreteModel()

        self.m.node_set = pyo.Set(initialize = self.node_set)
        self.m.edge_set = pyo.Set(initialize = self.edge_set,dimen = 2 )
        #Make rule that we cant send flow along an edge unless its X value is true 

        self.m.X = pyo.Var(self.m.edge_set,domain=pyo.NonNegativeReals) 
        self.m.Y = pyo.Var(self.m.edge_set,within = pyo.Binary )
      
        #Objective rule 
        def obj_rule(m):
            return sum( m.Y[e]* self.edge_data.loc[e]['weight'] for e in self.edge_set) 
        self.m.Obj = pyo.Objective(rule = obj_rule,sense = pyo.minimize)
      
        #Flow Conservation 
       
        def flow_conservation(m,n): 
            edges = self.edge_data.reset_index()
          
            incoming = edges[edges['edgeEnd'] ==n ]
            outgoing = edges[edges['edgeStart'] == n]
           
            return sum(m.X[(n,s[1]['edgeEnd'])] for s in outgoing.iterrows() ) - sum(m.X[(p[1]['edgeStart'],n)] for p in incoming.iterrows())    == self.node_data.loc[n]['imbalance']
        self.m.FlowCons = pyo.Constraint(self.m.node_set,rule = flow_conservation)
       
        def flow_along_active_edge(m,n,p):


            return m.X[n,p] <= self.edge_data.loc[n,p]['capacity'] * m.Y[n,p]
        self.m.activeEdges = pyo.Constraint(self.m.edge_set,rule=flow_along_active_edge)
        
        def capacity_constraints(m,n,p):
        
            return (0,m.X[n,p],self.edge_data.loc[n,p]['capacity'])
            
        self.m.capContraints = pyo.Constraint(self.m.edge_set,rule =capacity_constraints)
        
    def solve(self):
        solver = pyomo.opt.SolverFactory('glpk')
        results = solver.solve(self.m, tee=True, keepfiles=False)
        return results ,self.m
        

"""

If I am interpreting this correctly, I would suggest turning this around:

 if use=0 then flow=0
 else flow is unrestricted
This can be modeled as:

 flow <= cap*use

"""