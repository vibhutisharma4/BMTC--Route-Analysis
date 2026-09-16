import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import os

os.makedirs('outputs/figures', exist_ok=True)

routes = pd.read_csv('data/processed/routes_clustered.csv')

FEATURES = ['zone_enc', 'type_enc', 'name_length', 'origin_freq', 'dest_freq', 'is_premium']
X = routes[FEATURES].fillna(0)
X_scaled = StandardScaler().fit_transform(X)

iso = IsolationForest(contamination=0.05, random_state=42)
routes['is_anomaly'] = (iso.fit_predict(X_scaled) == -1).astype(int)

print(f'Anomalous routes: {routes["is_anomaly"].sum()}')
print(routes[routes['is_anomaly'] == 1][
    ['route_id', 'route_long_name', 'zone', 'route_type_label', 'origin_freq']
].head(10).to_string())

# MultiGraph, not Graph: multiple routes can share the same origin/destination
# pair (e.g. two different route_ids both running "Kempegowda - Whitefield").
# A plain Graph silently overwrites the earlier edge on add_edge(), so edge
# count stops equalling route count and route_id data gets lost. MultiGraph
# keeps every route as its own edge.
G = nx.MultiGraph()
for _, row in routes.dropna(subset=['origin', 'destination']).iterrows():
    if row['origin'] != row['destination']:
        G.add_edge(row['origin'], row['destination'], route_id=row['route_id'])

print(f'Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}')
print(f'(Edges should be close to len(routes) minus circular routes: {len(routes[routes["is_circular"]==0])})')

pr = nx.pagerank(G, alpha=0.85)
pr_df = pd.DataFrame(list(pr.items()), columns=['stop', 'pagerank'])
pr_df = pr_df.sort_values('pagerank', ascending=False).reset_index(drop=True)

print('\nTop 15 critical hubs by PageRank:')
print(pr_df.head(15).to_string())

plt.figure(figsize=(10, 6))
top15 = pr_df.head(15)
plt.barh(top15['stop'][::-1], top15['pagerank'][::-1], color='steelblue')
plt.title('Hub Criticality — PageRank Score')
plt.tight_layout()
plt.savefig('outputs/figures/pagerank.png', dpi=150)
plt.close()

deg_df = pd.DataFrame(
    list(nx.degree_centrality(G).items()),
    columns=['stop', 'degree_centrality']
).sort_values('degree_centrality', ascending=False)

print('\nTop 10 by degree centrality:')
print(deg_df.head(10).to_string())

routes.to_csv('data/processed/routes_final.csv', index=False)
pr_df.to_csv('data/processed/pagerank_scores.csv', index=False)
print("Done: 05_anomaly_network")