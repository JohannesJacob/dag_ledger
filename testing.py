
# Test
# https://github.com/iotaledger/iotavisualization/blob/master/src/shared/generateData.js
g = DAG()
g.genesis(5)
for i in range(1,5):
    letter = ['A', 'B', 'C', 'D']
    g.new_transaction({
        "sender": "initial_TX " + str(i), #"Person " + random.choice(letter),
        "receiver": "Person " + random.choice(letter),
        "amount": i*10})


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
plotnx = {}
for key in t.keys():
    plotnx[key] = t[key]['edges']

G = nx.DiGraph(plotnx)
pos = nx.draw_spring(G)
nx.draw(G, pos,  with_labels=True)
plt.show()

## Next test
df = pd.DataFrame({ 'from':['1', '2', '3', '4','5', '6', '6'], 'to':['0', '0', '0', '0','0','4', '3']})

G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

# Make the graph
nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True, node_color="skyblue", pos=nx.spectral_layout(G))
plt.title("spectral")
plt.show()