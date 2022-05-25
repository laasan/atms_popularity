import click
from dadata import Dadata
import json
import pandas as pd

TOKEN = "08e834c01c8911fb1b6b094f693320dd9384f64f"
SECRET = "78ddd9aa20281d96f879bc7e3394596bc23fb88c"


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def geocode_address(input_path: str, output_path: str):
    """Function determines the coordinates of the address (house, street, city)
    :param input_path: Path to read combined DataFrame
    :param output_path: Path to save geocoded addresses .json
    :return:
    """
    df = pd.read_csv(input_path)

    df = df.drop_duplicates(subset=["address"])
    geocoded_addresses = []
    raw_address = df["address"]
    with Dadata(TOKEN, SECRET) as dadata:
        for address in raw_address:
            response = dadata.clean(name="address", source=address)
            geocoded_addresses.append(response)

    with open(output_path, "w") as f:
        json.dump(geocoded_addresses, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    geocode_address()
