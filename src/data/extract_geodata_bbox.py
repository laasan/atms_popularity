import click
import geopandas as gpd

BBOX = (32.2, 41.14, 49.89, 58.26)


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def extract_geodata_bbox(input_path: str, output_path: str):
    """Function cut points inside the given bounding box
    :param input_path: Path to read full GeoDataFrame
    :param output_path: Path to save filtered GeoDataFrame
    :return:
    """
    gdf = gpd.read_file(input_path, bbox=BBOX)

    gdf.to_file(output_path, driver="GeoJSON")
    print(gdf.shape)


if __name__ == "__main__":
    extract_geodata_bbox()
