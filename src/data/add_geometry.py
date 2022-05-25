import click
import geopandas as gpd
import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def add_geometry(input_path: str, output_path: str):
    """Function converts DataFrame to GeoDataFrame with geometries
    :param input_path: Path to read main DataFrame
    :param output_path: Path to save GeoDataFrame
    :return:
    """
    df = pd.read_csv(input_path)

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df["geo_lon"], df["geo_lat"]), crs="epsg:4326"
    )

    gdf.to_file(output_path, driver="GeoJSON")
    print(gdf.shape)

if __name__ == "__main__":
    add_geometry()
