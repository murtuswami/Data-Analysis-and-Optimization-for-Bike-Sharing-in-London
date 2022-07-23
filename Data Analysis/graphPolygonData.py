import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 


with open('tripsEndingInPoly.txt') as f:
    lines = f.readlines()
tripsEndingInPoly = lines[0]

with open('tripsStartingInPoly.txt') as f: 
    lines = f.readlines()
tripsStartingInPoly = lines [0]

with open('demandInPolyAtTime.txt') as f:
    lines = f.readlines()
demandInPolyAtTime = lines[0]

hours = [x for x in range(0,24)]
tripsEndingInPoly = [int(x) for x in tripsEndingInPoly.split(",")]
tripsStartingInPoly = [int(x) for x in tripsStartingInPoly.split(",")]
demandInPolyAtTime = [int(x) for x in demandInPolyAtTime.split(",")]


print(tripsEndingInPoly,"\n",tripsStartingInPoly,"\n",demandInPolyAtTime)
demandFrame = pd.DataFrame({"Hour":hours, "Demand":demandInPolyAtTime})
tripsFrame = pd.DataFrame({"Hour":hours, "Trips Ending In Poly":tripsEndingInPoly,"Trips Starting In Poly":tripsStartingInPoly})
tripsStartingInPoly = pd.DataFrame({"Hour":hours, "Trips Starting In Poly":tripsStartingInPoly})
tripsFrame = pd.melt(tripsFrame, ['Hour'])
tripsFrame.rename(columns = {'variable' : 'Trip Type', 'value' : 'Trips'}, inplace = True)

print(tripsFrame)
sns.set_theme()
sns.set_context("paper")



#fig, ax =plt.subplots(1,2)
sns.lineplot(x='Hour', y='Trips', hue='Trip Type', data=tripsFrame).set(title="Trips In/Out of Polygon")
plt.xticks([i for i in range(0,24)])

plt.show()
plt.clf()
sns.lineplot(x="Hour",y="Demand",data = demandFrame).set(title="Cumulative Demand in Polygon")
plt.xticks([i for i in range(0,24)])
plt.show()
