import pandas as pd
import re
import os

os.makedirs('data/processed', exist_ok=True)

routes = pd.read_csv('data/raw/routes.csv')

routes = routes.drop(columns=['route_desc', 'route_url', 'route_color', 'route_text_color'], errors='ignore')

def split_origin_destination(name):
    if pd.isna(name) or ' - ' not in str(name):
        return pd.Series([None, None])
    origin, destination = str(name).split(' - ', 1)
    return pd.Series([origin.strip(), destination.strip()])

routes[['origin', 'destination']] = routes['route_long_name'].apply(split_origin_destination)
routes = routes.dropna(subset=['origin', 'destination'])

routes['name_length'] = routes['route_long_name'].str.len()
routes['is_circular'] = (routes['origin'] == routes['destination']).astype(int)

def classify_type(row):
    name = str(row['route_long_name'])
    route_id = str(row['route_id'])
    if 'Airport' in name:
        return 'Airport'
    if 'Vajra' in name:
        return 'Vajra'
    if 'Volvo' in name:
        return 'Volvo'
    if 'Express' in name:
        return 'Express'
    suffix = re.search(r'([A-Za-z]+)$', route_id)
    suffix = suffix.group(1) if suffix else ''
    if suffix == '':
        return 'Ordinary'
    if len(suffix) == 1:
        return 'Ordinary Variant'
    return 'Special'

routes['route_type_label'] = routes.apply(classify_type, axis=1)

# Central hubs are checked separately and LAST on purpose — see classify_zone().
# Almost every route in this network originates at one of these three hubs, so if
# Central were checked first (as it originally was), a route like
# "Kempegowda Bus Station - Nagarbhavi" would be mislabeled Central just because
# the origin matches, even though the destination is clearly West.
CENTRAL_KEYWORDS = ['Kempegowda', 'Krishnarajendra', 'KR Market', 'Shivajinagar', 'Majestic', 'Chickpet']

ZONE_KEYWORDS = {
    'North':   ['Yelahanka', 'Hebbal', 'Jalahalli', 'Peenya', 'Vidyaranyapura'],
    'South':   ['Jayanagar', 'Banashankari', 'JP Nagar', 'Basavangudi', 'Kengeri'],
    'East':    ['ITPL', 'Whitefield', 'Kadugodi', 'Hoskote', 'KR Puram'],
    'West':    [
        'Vijayanagar', 'Rajajinagar', 'Nagarbhavi', 'Nayandahalli',
        'Marappana Palya', 'Malleshwaram', 'Yeshwanthpur', 'Kamakshipalya',
        'Sunkadakatte', 'Ullal', 'Andrahalli', 'Okalipuram',
    ],
}

def classify_zone(row):
    origin = str(row['origin']).lower()
    destination = str(row['destination']).lower()
    text = f"{origin} {destination}"

    # 1. Check peripheral zones against the FULL text first. This lets a route
    #    like "Kempegowda Bus Station - Nagarbhavi" classify as West even though
    #    the origin is a Central hub — the destination is what tells you where
    #    the route actually goes.
    for zone, keywords in ZONE_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            return zone

    # 2. Only fall back to Central if nothing peripheral matched — i.e. both
    #    ends of the route are genuinely central (e.g. "Kempegowda - KR Market").
    if any(kw.lower() in text for kw in CENTRAL_KEYWORDS):
        return 'Central'

    return 'Other'

routes['zone'] = routes.apply(classify_zone, axis=1)

print('Route type distribution:')
print(routes['route_type_label'].value_counts())
print()
print('Zone distribution:')
print(routes['zone'].value_counts())
print()
print(f'Circular routes: {routes["is_circular"].sum()}')

routes.to_csv('data/processed/routes_clean.csv', index=False)
print("Done: 01_data_cleaning")
