"""
06_generate_dashboard_data.py

Builds data.js from the pipeline's actual output CSVs (routes_final.csv,
pagerank_scores.csv). This did not exist before — the dashboard's data.js
was hand-authored placeholder numbers that never matched what the scripts
actually produced. This script closes that gap: run it last, after
anamoly_network.py, and data.js will always reflect the real pipeline output.
"""
import pandas as pd
import json
import os

routes = pd.read_csv('data/processed/routes_final.csv')
pagerank = pd.read_csv('data/processed/pagerank_scores.csv')

ZONE_COLORS = {
    'Central': '#f7c948', 'South': '#3dd68c', 'North': '#6eb5ff',
    'East': '#ff6b6b', 'West': '#b48eff', 'Other': '#6b7592'
}
TYPE_COLORS = {
    'Special': '#6eb5ff', 'Ordinary': '#f7c948', 'Ordinary Variant': '#3dd68c',
    'Express': '#b48eff', 'Volvo': '#ff9f43', 'Vajra': '#ff6b6b', 'Airport': '#a8e063'
}
CLUSTER_COLORS = ['#f7c948', '#6eb5ff', '#3dd68c', '#ff6b6b', '#b48eff', '#a8e063']

# ---- zones ----
zones = routes['zone'].value_counts().to_dict()

# ---- route types ----
route_types = {
    t: {'count': int(c), 'color': TYPE_COLORS.get(t, '#6b7592')}
    for t, c in routes['route_type_label'].value_counts().items()
}

# ---- top hubs: real stop frequency, origin + destination combined ----
stop_freq = pd.concat([
    routes[['origin']].rename(columns={'origin': 'stop'}),
    routes[['destination']].rename(columns={'destination': 'stop'})
])['stop'].value_counts()
top_hubs = [{'name': s, 'routes': int(c)} for s, c in stop_freq.head(12).items()]

# ---- clusters ----
clusters = []
for i, (cid, g) in enumerate(sorted(routes.groupby('cluster'))):
    label = g['cluster_label'].iloc[0]
    samples = g['route_long_name'].sample(min(3, len(g)), random_state=42).tolist()
    clusters.append({
        'id': int(cid),
        'size': int(len(g)),
        'label': label,
        'color': CLUSTER_COLORS[i % len(CLUSTER_COLORS)],
        'top_zone': g['zone'].mode()[0],
        'top_type': g['route_type_label'].mode()[0],
        'avg_name_len': round(float(g['name_length'].mean()), 1),
        'desc': f"{label} — {len(g)} routes, avg origin frequency {g['origin_freq'].mean():.0f}.",
        'samples': samples
    })

# ---- anomalies ----
anom = routes[routes['is_anomaly'] == 1].copy()

# Most-flagged type/zone computed from the FULL 214-route anomaly set, not just
# the 8-item sample shown on the page — anamolies.html used to hardcode
# "Volvo" / "Central" here without checking against the real distribution.
most_flagged_type = anom['route_type_label'].mode()[0]
most_flagged_zone = anom['zone'].mode()[0]

anom_sample = anom.sample(min(8, len(anom)), random_state=42)
anomalies = [{
    'route_id': r['route_id'],
    'name': r['route_long_name'],
    'zone': r['zone'],
    'type': r['route_type_label'],
    'origin_freq': int(r['origin_freq'])
} for _, r in anom_sample.iterrows()]

# ---- coverage ----
coverage_counts = routes['coverage_level'].value_counts()
coverage = {
    lvl: {'count': int(coverage_counts.get(lvl, 0)), 'desc': desc}
    for lvl, desc in [
        ('High', 'Served by 100+ routes'),
        ('Moderate', 'Served by 20-99 routes'),
        ('Low', 'Served by 5-19 routes'),
        ('Underserved', 'Served by only 1 route'),
    ]
}

underserved_stops = stop_freq[stop_freq == 1].index.tolist()
underserved_sample = pd.Series(underserved_stops).sample(
    min(10, len(underserved_stops)), random_state=42
).tolist()

# ---- graph stats (real counts, used to be hardcoded "~2,400" etc in network.html) ----
graph_nodes = int(stop_freq.shape[0])
graph_edges = int((routes['is_circular'] == 0).sum())

# ---- coverage insight stats (used to be hardcoded in coverage.html) ----
top2_hub_routes = int(sum(h['routes'] for h in top_hubs[:2]))
top2_hub_share_pct = round(top2_hub_routes / len(routes) * 100, 1)
underserved_share_pct = round(len(underserved_stops) / graph_nodes * 100, 1)

# ---- pagerank top hubs (real network centrality, not just route count) ----
pagerank_top = pagerank.sort_values('pagerank', ascending=False).head(15)
pagerank_hubs = [
    {
        'name': r['stop'],
        'pagerank': round(float(r['pagerank']), 5),
        'routes': int(stop_freq.get(r['stop'], 0))  # route count for context, ranking stays by pagerank
    }
    for _, r in pagerank_top.iterrows()
]

# ---- zone x type matrix (routes.html hardcoded this before; now it's real) ----
PREMIUM_TYPES = ['Vajra', 'Volvo', 'Airport']
matrix = []
for zone in sorted(routes['zone'].unique(), key=lambda z: -zones.get(z, 0)):
    zg = routes[routes['zone'] == zone]
    matrix.append({
        'zone': zone,
        'ord': int((zg['route_type_label'] == 'Ordinary').sum()),
        'var': int((zg['route_type_label'] == 'Ordinary Variant').sum()),
        'spe': int((zg['route_type_label'] == 'Special').sum()),
        'exp': int((zg['route_type_label'] == 'Express').sum()),
        'prem': int(zg['route_type_label'].isin(PREMIUM_TYPES).sum()),
        'total': int(len(zg)),
    })

# ---- circular route samples (real ones, not hand-typed) ----
circ = routes[routes['is_circular'] == 1]
circular_samples = circ['route_long_name'].sample(min(7, len(circ)), random_state=42).tolist()

DATA = {
    'zones': zones,
    'zone_type_matrix': matrix,
    'circular_samples': circular_samples,
    'zone_colors': ZONE_COLORS,
    'route_types': route_types,
    'top_hubs': top_hubs,
    'pagerank_hubs': pagerank_hubs,
    'clusters': clusters,
    'anomalies': anomalies,
    'coverage': coverage,
    'underserved_sample': underserved_sample,
    'total_routes': int(len(routes)),
    'circular_routes': int(routes['is_circular'].sum()),
    'graph_nodes': graph_nodes,
    'graph_edges': graph_edges,
    'top2_hub_routes': top2_hub_routes,
    'top2_hub_share_pct': top2_hub_share_pct,
    'underserved_share_pct': underserved_share_pct,
    'anomaly_count': int(len(anom)),
    'contamination_pct': round(len(anom) / len(routes) * 100, 1),
    'most_flagged_type': most_flagged_type,
    'most_flagged_zone': most_flagged_zone,
}

os.makedirs('frontend', exist_ok=True)
with open('frontend/data.js', 'w') as f:
    f.write('const DATA = ' + json.dumps(DATA, indent=2) + ';\n')

print(f"Wrote frontend/data.js")
print(f"  zones: {zones}")
print(f"  total_routes: {DATA['total_routes']}, circular: {DATA['circular_routes']}")
print(f"  anomalies sampled: {len(anomalies)}, clusters: {len(clusters)}")
print("Done: 06_generate_dashboard_data")
