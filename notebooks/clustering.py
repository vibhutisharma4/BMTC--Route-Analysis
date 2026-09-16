import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

os.makedirs('outputs/figures', exist_ok=True)

routes = pd.read_csv('data/processed/routes_features.csv')

FEATURES = ['zone_enc', 'type_enc', 'name_length', 'origin_freq', 'dest_freq', 'is_premium']
X = routes[FEATURES].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(range(2, 10), inertias, marker='o')
plt.axvline(x=4, color='red', linestyle='--', label='K=4 chosen')
plt.title('Elbow Method')
plt.xlabel('K')
plt.ylabel('Inertia')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/figures/elbow.png', dpi=150)
plt.close()

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
routes['cluster'] = kmeans.fit_predict(X_scaled)

# Label clusters from their actual contents rather than assuming KMeans always
# assigns IDs 0-3 in the same semantic order. random_state=42 makes IDs
# deterministic for a FIXED input, but if the upstream data changes (e.g. a
# zone-classification fix shifts which routes are Central vs peripheral),
# cluster 0 is no longer guaranteed to be "Peripheral Special Routes" — a
# hardcoded {0: '...'} map would then mislabel silently. This inspects each
# cluster's real top zone/type/hub and builds a descriptive name from that.
def name_cluster(cluster_id, group):
    top_zone = group['zone'].mode()[0]
    top_type = group['route_type_label'].mode()[0]
    premium_share = group['is_premium'].mean()
    avg_freq = group['origin_freq'].mean()

    # Special-case: a cluster dominated by one non-mega-hub origin (e.g. a
    # secondary bus station) is a "corridor" cluster in its own right.
    hub_counts = group['origin'].value_counts()
    top_hub = hub_counts.index[0] if len(hub_counts) else None
    top_hub_share = hub_counts.iloc[0] / len(group) if len(hub_counts) else 0
    MEGA_HUBS = ('Kempegowda Bus Station', 'Krishnarajendra Market')

    if top_hub and top_hub_share > 0.5 and top_hub not in MEGA_HUBS:
        return f'{top_hub} Corridor'
    if premium_share > 0.5:
        return 'Premium Service Routes'
    if top_zone == 'Central':
        # Two Central-dominant clusters can differ a lot in whether they
        # actually run through Kempegowda/KR Market (high origin_freq) or
        # just terminate somewhere central without passing through the
        # mega-hubs (low origin_freq) — origin_freq is what tells them apart.
        return 'Central Mega-Hub Routes' if avg_freq > 300 else 'Central Secondary Routes'
    return f'Peripheral {top_type} Routes'

cluster_labels = {
    cid: name_cluster(cid, group)
    for cid, group in routes.groupby('cluster')
}
routes['cluster_label'] = routes['cluster'].map(cluster_labels)
print('Cluster labels (derived from data, not hardcoded):', cluster_labels)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
colors = ['#f7c948', '#6eb5ff', '#3dd68c', '#ff6b6b']

plt.figure(figsize=(10, 7))
for i, label in cluster_labels.items():
    mask = routes['cluster'] == i
    plt.scatter(X_pca[mask, 0], X_pca[mask, 1], c=colors[i], label=label, alpha=0.5, s=10)
plt.title('Route Clusters (PCA 2D)')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/figures/clusters_pca.png', dpi=150)
plt.close()

print(routes.groupby('cluster_label').agg(
    count=('route_id', 'count'),
    top_zone=('zone', lambda x: x.mode()[0]),
    top_type=('route_type_label', lambda x: x.mode()[0]),
    avg_name_len=('name_length', 'mean'),
    avg_origin_freq=('origin_freq', 'mean')
).round(2).to_string())

routes.to_csv('data/processed/routes_clustered.csv', index=False)
print("Done: 04_clustering")