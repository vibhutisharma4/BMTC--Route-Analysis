import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os
os.makedirs('outputs/figures', exist_ok=True) if not os.path.exists('outputs/figures') else None

routes = pd.read_csv('data/processed/routes_clean.csv')

all_stops = list(routes['origin'].dropna()) + list(routes['destination'].dropna())
stop_freq = Counter(all_stops)
top20 = pd.DataFrame(stop_freq.most_common(20), columns=['stop', 'count'])

plt.figure(figsize=(10, 7))
sns.barplot(data=top20, x='count', y='stop', hue='stop', palette='magma', legend=False)
plt.title('Top 20 Terminal Hubs')
plt.tight_layout()
plt.savefig('outputs/figures/top_hubs.png', dpi=150)
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
zone_counts = routes['zone'].value_counts()
axes[0].pie(zone_counts.values, labels=zone_counts.index, autopct='%1.1f%%')
axes[0].set_title('Routes by Zone')

type_counts = routes['route_type_label'].value_counts()
sns.barplot(x=type_counts.values, y=type_counts.index, hue=type_counts.index, ax=axes[1], palette='viridis', legend=False)
axes[1].set_title('Routes by Service Type')
plt.tight_layout()
plt.savefig('outputs/figures/zone_type.png', dpi=150)
plt.close()

freq_vals = pd.Series(list(stop_freq.values()))
underserved = sum(1 for v in stop_freq.values() if v == 1)
print(f'Stops served by only 1 route: {underserved}')
print(f'Stops served by 10+ routes:   {sum(1 for v in stop_freq.values() if v >= 10)}')

freq_vals.clip(upper=50).hist(bins=30, color='steelblue', edgecolor='white', figsize=(10, 4))
plt.title('Routes per Stop Distribution (clipped at 50)')
plt.tight_layout()
plt.savefig('outputs/figures/coverage_dist.png', dpi=150)
plt.close()

circular = routes[routes['is_circular'] == 1]
print(f'Circular routes: {len(circular)}')
print(circular[['route_id', 'route_long_name', 'zone']].head(10))
print("Done: 02_eda")