import click
import geopandas as gpd


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def turn_poi(input_paths: str, output_path: str):
    """

    :param input_paths:
    :param output_path:
    :return:
    """
    pois = gpd.read_file(input_paths[0])
    gdf = gpd.read_file(input_paths[1])

    pois.loc[pois["shop"].notna(), "shop"] = "shop"
    pois["poi_type"] = pois["amenity"]
    pois["poi_type"] = pois["poi_type"].fillna(pois["shop"])
    pois["poi_type"] = pois["poi_type"].fillna(pois["highway"])
    pois["poi_type"] = pois["poi_type"].fillna(pois["tourism"])
    pois["poi_type"] = pois["poi_type"].fillna(pois["building"])
    pois.drop(
        columns=["amenity", "building", "highway", "shop", "tourism"], inplace=True
    )

    gdf = gdf.to_crs("epsg:3395")
    gdf["poi_buffer"] = gdf.buffer(200)
    gdf = gdf.set_geometry("poi_buffer")
    gdf = gdf.to_crs("epsg:4326")
    gdf_pois = gpd.sjoin(gdf, pois, how="left", predicate="intersects")
    gdf_pois = gdf_pois.groupby(["id", "poi_type"], as_index=False).agg(
        poi_cnt=("index_right", "count")
    )
    gdf_pois = (
        gdf_pois.pivot(index=["id"], columns="poi_type", values="poi_cnt")
        .fillna(0)
        .reset_index()
    )

    gdf_pois.to_csv(output_path, index=False)


if __name__ == "__main__":
    turn_poi()
