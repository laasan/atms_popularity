import click
import geopandas as gpd


@click.command()
@click.argument("bbox", type=click.FLOAT, nargs=4)
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def bbox_geodata(bbox: list[float], input_path: str, output_path: str):
    """Function cut points inside the given bounding box
    :param bbox: Corners coordinates of bounding box
    :param input_path: Path to read full GeoDataFrame
    :param output_path: Path to save filtered GeoDataFrame
    :return:
    """
    gdf = gpd.read_file(input_path, bbox=tuple(bbox))

    gdf.to_file(output_path, driver="GeoJSON")
    print(gdf.shape)


if __name__ == "__main__":
    bbox_geodata()
