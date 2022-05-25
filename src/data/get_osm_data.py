import click
import pyrosm


@click.command()
@click.argument("region")
@click.argument("directory")
def get_osm_data(region: str, directory: str):
    """Function downloads extract from the OpenStreetMap project in the selected region
    :param region: Region name
    :param directory: Directory to save OSM data
    :return:
    """
    fp = pyrosm.get_data(region, directory=directory)
    print("Data was downloaded to:", fp)


if __name__ == "__main__":
    get_osm_data()
