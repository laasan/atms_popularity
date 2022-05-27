import click
import geopandas as gpd
from pyrosm import OSM
import warnings

warnings.filterwarnings("ignore")


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def near_atms_dist(input_paths: list[str], output_path: str):
    """Function finds the distance to the nearest ATM on the osm map
    :param input_paths: Paths to read main GeoDataFrame and OSM dump
    :param output_path: Path to save the nearest ATM feature DataFrame
    :return:
    """
    gdf = gpd.read_file(input_paths[0])
    osm = OSM(input_paths[1])

    osm_keys_to_keep = ["amenity"]
    custom_filter = {"amenity": ["atm"]}
    atms = osm.get_data_by_custom_criteria(
        osm_keys_to_keep=osm_keys_to_keep, custom_filter=custom_filter
    )
    atms = atms[["amenity", "geometry"]]
    atms = atms.to_crs("epsg:3395")
    gdf = gdf.to_crs("epsg:3395")
    nearest_atm = gdf.sjoin_nearest(atms, how="left", distance_col="near_atm_dist")
    nearest_atm = nearest_atm[["id", "near_atm_dist"]]

    nearest_atm.to_csv(output_path, index=False)


if __name__ == "__main__":
    near_atms_dist()
