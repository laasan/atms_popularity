import click
from dadata import Dadata
import pandas as pd

TOKEN = "08e834c01c8911fb1b6b094f693320dd9384f64f"
SECRET = "78ddd9aa20281d96f879bc7e3394596bc23fb88c"


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def gaps_geocoding(input_path: str, output_path: str):
    """Function tries to get missing coordinates from raw address via DaData API
    :param input_path: Path to read DataFrame with missing coordinates
    :param output_path: Path to save geocoded DataFrame
    :return:
    """
    geocoded_df = pd.DataFrame()
    missing_coordinates_df = pd.read_csv(input_path, index_col=0)

    with Dadata(TOKEN, SECRET) as dadata:
        for x in missing_coordinates_df["address"]:
            response = dadata.clean(name="address", source=x)
            response = pd.DataFrame.from_dict([response])
            geocoded_df = pd.concat([geocoded_df, response])

    geocoded_df.to_csv(output_path)


if __name__ == "__main__":
    gaps_geocoding()
