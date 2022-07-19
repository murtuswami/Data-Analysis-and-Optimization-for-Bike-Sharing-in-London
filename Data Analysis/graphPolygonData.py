import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 


with open('tripsintopoly.txt') as f:
    lines = f.readlines()
bikesIntoPoly = lines[0]

with open('tripsoutofpoly.txt') as f: 
    lines = f.readlines()
bikesOutOfPoly = lines [0]

with open('tripswithinpoly.txt') as f:
    lines = f.readlines()
bikesWithinPoly = lines[0]

hours = [x for x in range(1,24)]
bikesIntoPoly = [int(x) for x in bikesIntoPoly.split(",")]
bikesOutOfPoly = [int(x) for x in bikesOutOfPoly.split(",")]
bikesWithinPoly = [int(x) for x in bikesWithinPoly.split(",")]


print(bikesIntoPoly,"\n",bikesOutOfPoly,"\n",bikesWithinPoly)

supplyInPoly = []
supply = 0 
for n,x in enumerate(bikesIntoPoly):
    supplyInPoly.append(supply + x - bikesOutOfPoly[n] )
print(supplyInPoly)

bikesIntoPoly = pd.DataFrame({"Hour":hours, "Supply":bikesOutOfPoly})
bikesOutOfPoly = pd.DataFrame({"Hour":hours, "Demand":bikesOutOfPoly})


fig, ax =plt.subplots(1,2)
sns.lineplot(x ="Hour" , y="Supply" ,data = bikesIntoPoly, ax=ax[0])
sns.lineplot(x ="Hour" , y="Demand" ,data = bikesOutOfPoly, ax=ax[1])
fig.show()
plt.show()
plt.clear()
