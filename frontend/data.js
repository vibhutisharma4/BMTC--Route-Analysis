const DATA = {
  "zones": {
    "Central": 2265,
    "Other": 1020,
    "South": 382,
    "North": 328,
    "East": 177,
    "West": 99
  },
  "zone_type_matrix": [
    {
      "zone": "Central",
      "ord": 315,
      "var": 1566,
      "spe": 368,
      "exp": 0,
      "prem": 16,
      "total": 2265
    },
    {
      "zone": "Other",
      "ord": 177,
      "var": 259,
      "spe": 580,
      "exp": 4,
      "prem": 0,
      "total": 1020
    },
    {
      "zone": "South",
      "ord": 91,
      "var": 147,
      "spe": 142,
      "exp": 0,
      "prem": 2,
      "total": 382
    },
    {
      "zone": "North",
      "ord": 48,
      "var": 124,
      "spe": 156,
      "exp": 0,
      "prem": 0,
      "total": 328
    },
    {
      "zone": "East",
      "ord": 27,
      "var": 79,
      "spe": 69,
      "exp": 0,
      "prem": 2,
      "total": 177
    },
    {
      "zone": "West",
      "ord": 12,
      "var": 40,
      "spe": 46,
      "exp": 0,
      "prem": 1,
      "total": 99
    }
  ],
  "circular_samples": [
    "Jayanagara 4th Block - Jayanagara 4th Block",
    "Banashankari Bus Station - Banashankari Bus Station",
    "Vasanthapura - Vasanthapura",
    "Kempegowda Bus Station - Kempegowda Bus Station",
    "Tin Factory - Tin Factory",
    "Kempegowda Bus Station - Kempegowda Bus Station",
    "Banashankari Bus Station - Banashankari Bus Station"
  ],
  "zone_colors": {
    "Central": "#f7c948",
    "South": "#3dd68c",
    "North": "#6eb5ff",
    "East": "#ff6b6b",
    "West": "#b48eff",
    "Other": "#6b7592"
  },
  "route_types": {
    "Ordinary Variant": {
      "count": 2215,
      "color": "#3dd68c"
    },
    "Special": {
      "count": 1361,
      "color": "#6eb5ff"
    },
    "Ordinary": {
      "count": 670,
      "color": "#f7c948"
    },
    "Airport": {
      "count": 18,
      "color": "#a8e063"
    },
    "Express": {
      "count": 4,
      "color": "#b48eff"
    },
    "Vajra": {
      "count": 3,
      "color": "#ff6b6b"
    }
  },
  "top_hubs": [
    {
      "name": "Kempegowda Bus Station",
      "routes": 1028
    },
    {
      "name": "Krishnarajendra Market",
      "routes": 1004
    },
    {
      "name": "Shivajinagar Bus Station",
      "routes": 418
    },
    {
      "name": "Banashankari Bus Station",
      "routes": 89
    },
    {
      "name": "Kadugodi",
      "routes": 86
    },
    {
      "name": "BANASHANKARI TTMC",
      "routes": 76
    },
    {
      "name": "Kengeri TTMC",
      "routes": 62
    },
    {
      "name": "Yelahanka",
      "routes": 61
    },
    {
      "name": "ITPL",
      "routes": 54
    },
    {
      "name": "Electronic City Wipro Gate",
      "routes": 53
    },
    {
      "name": "Central Silk Board",
      "routes": 52
    },
    {
      "name": "Hosakote Bus Stand",
      "routes": 49
    }
  ],
  "pagerank_hubs": [
    {
      "name": "Krishnarajendra Market",
      "pagerank": 0.12827
    },
    {
      "name": "Kempegowda Bus Station",
      "pagerank": 0.10318
    },
    {
      "name": "Shivajinagar Bus Station",
      "pagerank": 0.04145
    },
    {
      "name": "Kadugodi",
      "pagerank": 0.00789
    },
    {
      "name": "Banashankari Bus Station",
      "pagerank": 0.00591
    },
    {
      "name": "Kengeri TTMC",
      "pagerank": 0.00556
    },
    {
      "name": "Yelahanka",
      "pagerank": 0.00536
    },
    {
      "name": "BANASHANKARI TTMC",
      "pagerank": 0.00536
    },
    {
      "name": "ITPL",
      "pagerank": 0.00508
    },
    {
      "name": "Electronic City Wipro Gate",
      "pagerank": 0.00481
    },
    {
      "name": "Central Silk Board",
      "pagerank": 0.00469
    },
    {
      "name": "Hosakote Bus Stand",
      "pagerank": 0.00462
    },
    {
      "name": "Nelamangala",
      "pagerank": 0.00427
    },
    {
      "name": "Hebbala",
      "pagerank": 0.00404
    },
    {
      "name": "Manyatha Embasy Business Park",
      "pagerank": 0.00394
    }
  ],
  "clusters": [
    {
      "id": 0,
      "size": 1456,
      "label": "Central Mega-Hub Routes",
      "color": "#f7c948",
      "top_zone": "Central",
      "top_type": "Ordinary Variant",
      "avg_name_len": 40.0,
      "desc": "Central Mega-Hub Routes \u2014 1456 routes, avg origin frequency 930.",
      "samples": [
        "Krishnarajendra Market - Panathuru",
        "Krishnarajendra Market - Hosakote Bus Stand",
        "Krishnarajendra Market - Gollahalli"
      ]
    },
    {
      "id": 1,
      "size": 1883,
      "label": "Peripheral Special Routes",
      "color": "#6eb5ff",
      "top_zone": "Other",
      "top_type": "Special",
      "avg_name_len": 35.7,
      "desc": "Peripheral Special Routes \u2014 1883 routes, avg origin frequency 28.",
      "samples": [
        "Chowdeshwari Bus Stop - Cap Gemini",
        "Malleshwaram 18th Cross - Kadugodi",
        "Chandapura - MEI Layout"
      ]
    },
    {
      "id": 2,
      "size": 907,
      "label": "Central Secondary Routes",
      "color": "#3dd68c",
      "top_zone": "Central",
      "top_type": "Ordinary Variant",
      "avg_name_len": 41.8,
      "desc": "Central Secondary Routes \u2014 907 routes, avg origin frequency 43.",
      "samples": [
        "Kannamangala - Kempegowda Bus Station",
        "Shankararnag Bus Stop - Kempegowda Bus Station",
        "Jakkanahalli - Krishnarajendra Market"
      ]
    },
    {
      "id": 3,
      "size": 25,
      "label": "Premium Service Routes",
      "color": "#ff6b6b",
      "top_zone": "Central",
      "top_type": "Airport",
      "avg_name_len": 46.9,
      "desc": "Premium Service Routes \u2014 25 routes, avg origin frequency 100.",
      "samples": [
        "BANASHANKARI TTMC - Kempegowda International Airport",
        "Indian Express - Nagavara",
        "Krishnarajendra Market - Vajramuneshwara Temple"
      ]
    }
  ],
  "anomalies": [
    {
      "route_id": "S-18",
      "name": "Jayanagara 9th Block - Kempegowda Bus Station",
      "zone": "South",
      "type": "Ordinary",
      "origin_freq": 38
    },
    {
      "route_id": "KIAS-8",
      "name": "Electronic City - Kempegowda International Airport",
      "zone": "Central",
      "type": "Airport",
      "origin_freq": 30
    },
    {
      "route_id": "MLP-KBS",
      "name": "Malleshwaram 8th Main - Kempegowda Bus Station",
      "zone": "West",
      "type": "Special",
      "origin_freq": 3
    },
    {
      "route_id": "CS-13E",
      "name": "Banashankari 3rd Stage 2nd Phase - Shivajinagar Bus Station",
      "zone": "South",
      "type": "Ordinary Variant",
      "origin_freq": 12
    },
    {
      "route_id": "96A",
      "name": "Kempegowda Bus Station - Kempegowda Bus Station",
      "zone": "Central",
      "type": "Ordinary Variant",
      "origin_freq": 1028
    },
    {
      "route_id": "KIAS-7A",
      "name": "HSR BDA COMPLEX - Kempegowda International Airport",
      "zone": "Central",
      "type": "Airport",
      "origin_freq": 5
    },
    {
      "route_id": "60-A",
      "name": "JP Nagar 6th Phase - Krishnarajendra Market",
      "zone": "South",
      "type": "Ordinary Variant",
      "origin_freq": 7
    },
    {
      "route_id": "271",
      "name": "Jalahalli East Area 7th camp - Kempegowda Bus Station",
      "zone": "North",
      "type": "Ordinary",
      "origin_freq": 1
    }
  ],
  "coverage": {
    "High": {
      "count": 37,
      "desc": "Served by 100+ routes"
    },
    "Moderate": {
      "count": 531,
      "desc": "Served by 20-99 routes"
    },
    "Low": {
      "count": 1340,
      "desc": "Served by 5-19 routes"
    },
    "Underserved": {
      "count": 2363,
      "desc": "Served by only 1 route"
    }
  },
  "underserved_sample": [
    "Yattukodi",
    "ITI Layout Mallathahalli",
    "Horamavu",
    "Karahalli Cross",
    "Bande Bommasandra",
    "MVJ Medical Hospital",
    "ITI Gate",
    "KP Agrahara 16th cross",
    "Vabasandra",
    "Kodigehalli gate"
  ],
  "total_routes": 4271,
  "circular_routes": 114,
  "graph_nodes": 1728,
  "graph_edges": 4157,
  "top2_hub_routes": 2032,
  "top2_hub_share_pct": 47.6,
  "underserved_share_pct": 46.2,
  "anomaly_count": 214,
  "contamination_pct": 5.0,
  "most_flagged_type": "Ordinary",
  "most_flagged_zone": "Central"
};
