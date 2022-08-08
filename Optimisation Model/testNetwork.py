import pandas as pd
from minCostFlowSolver import MinCostFlow
from FeasibleFlowModel import FeasibleFlow
from pyomo.environ import value
import pdb
import numpy as np
import pickle
from TSPOR import TSPORSolver
"""
id = ['1','2','3','4','5','6']
imbalance = [5.0,0.0,0.0,0.0,0.0,-5]
d = {'id':id,'imbalance':imbalance}
nodes =pd.DataFrame(data = d)
nodes['id'] = nodes['id'].astype(np.unicode_)#
nodes = nodes.set_index('id')

startId = ['1','1','2','2','3','3','4','5'] ## problem is yo udoubled the indexes here cause u though its weights 
endId = ['2','3','4','5','4','5','6','6']
weights = [1.0,2.0,1.0,2.0,2.0,2.0,2.0,2.0]
capacity = [5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0]

d = {'edgeStart':startId,'edgeEnd':endId,'weight':weights,'capacity':capacity}

edges = pd.DataFrame(data = d)
edges['edgeStart'] = edges['edgeStart'].astype(np.unicode_)
edges['edgeEnd'] = edges['edgeEnd'].astype(np.unicode_)    
edges = edges.set_index(['edgeStart','edgeEnd'])
print(edges,nodes)


solver = FeasibleFlow(nodes,edges)
solver.makeModel()
results,model = solver.solve()

model.display()

newEdges = []

#new Edges is the edges we must have in the solution 


solver = MinCostFlow(nodesDF=nodes.copy(),edgesDF=edges.copy())
solver.makeModel()
results,model = solver.solve()
print(results,model)

print("Print values for each variable explicitly")
"""

with open('keyEdgesDict.p', 'rb') as fp:
    keyEdges = pickle.load(fp)
with open('edgesDict.p','rb') as fp:
    allEdges = pickle.load(fp)


TSPSolver = TSPORSolver(keyEdges,allEdges)
cost,route = TSPSolver.solve()

print(cost,route)