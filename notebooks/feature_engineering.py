import pandas as pd
from collections import Counter
from sklearn.preprocessing import LabelEncoder
import os

os.makedirs('data/processed', exist_ok=True)

routes = pd.read_csv('data/processed/routes_clean.csv')

all_stops = list(routes['origin'].dropna()) + list(routes['destination'].dropna())
stop_freq = Counter(all_stops)

routes['origin_freq']   = routes['origin'].map(stop_freq).fillna(0)
routes['dest_freq']     = routes['destination'].map(stop_freq).fillna(0)
routes['max_stop_freq'] = routes[['origin_freq', 'dest_freq']].max(axis=1)
routes['min_stop_freq'] = routes[['origin_freq', 'dest_freq']].min(axis=1)

def coverage_level(freq):
    # Underserved now means EXACTLY 1 route (freq < 2) — matches coverage.html's
    # description "Only 1 route. Zero alternatives for residents." Before,
    # this bucket included freq 1-4, so a stop with 4 routes was being called
    # "zero alternatives," which contradicted the page's own text.
    if freq >= 100: return 'High'
    if freq >= 20:  return 'Moderate'
    if freq >= 2:   return 'Low'
    return 'Underserved'

routes['coverage_level'] = routes['min_stop_freq'].apply(coverage_level)

le_zone = LabelEncoder()
le_type = LabelEncoder()
routes['zone_enc'] = le_zone.fit_transform(routes['zone'].fillna('Other'))
routes['type_enc'] = le_type.fit_transform(routes['route_type_label'])

routes['is_premium'] = routes['route_type_label'].isin(
    ['Vajra', 'Volvo', 'Airport', 'Express']
).astype(int)

print(routes['coverage_level'].value_counts())
routes.to_csv('data/processed/routes_features.csv', index=False)
print("Done: 03_feature_engineering")