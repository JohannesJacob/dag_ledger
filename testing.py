
# Test
# https://github.com/iotaledger/iotavisualization/blob/master/src/shared/generateData.js
g = DAG()
g.genesis(5)
for i in range(1,5):
    letter = ['A', 'B', 'C', 'D']
    g.new_transaction({
        "sender": "initial_TX " + str(i), #"Person " + random.choice(letter),
        "receiver": "Person " + random.choice(letter),
        "amount": float(i)})
g
cw = g.cum_weight()
import networkx as nx
import matplotlib.pyplot as plt
plotnx = {}
for key in t.keys():
    plotnx[key] = t[key]['edges']

G = nx.DiGraph(plotnx)
pos = nx.draw_spring(G)
nx.draw(G, pos,  with_labels=True)
plt.show()