import folium
from folium.plugins import MarkerCluster
import pandas as pd


def folium_map(df, pois):
    folium_df = df.merge(pois, how="left", on="id")
    lat = folium_df["geo_lat"]
    lon = folium_df["geo_lon"]
    m = folium.Map(
        location=[64.6863136, 97.7453061], zoom_start=3, tiles="Cartodb Positron"
    )
    marker_cluster = MarkerCluster().add_to(m)
    for lat, lon in zip(lat, lon):
        folium.Marker(
            location=[lat, lon],
            radius=8,
        ).add_to(marker_cluster)
    return m
