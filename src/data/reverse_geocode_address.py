import click
from dadata import Dadata
import json
import pandas as pd

TOKEN = "08e834c01c8911fb1b6b094f693320dd9384f64f"
SECRET = "78ddd9aa20281d96f879bc7e3394596bc23fb88c"


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def reverse_geocode_address(input_path: str, output_path: str):
    """Function finds the address by geographical coordinates.
    The structured address is needed to create features
    :param input_path: Path to read main DataFrame
    :param output_path: Path to save .json with reverse geocoded data
    :return:
    """
    df = pd.read_csv(input_path)
    df = df.drop_duplicates(subset=['lat', 'long'])

    response = []
    lat = df["lat"]
    lon = df["long"]
    with Dadata(TOKEN) as dadata:
        for lat, lon in zip(lat, lon):
            result = dadata.geolocate(name="address", lat=lat, lon=lon, count=1)
            if result:
                result[0].update({'lat': lat, 'long': lon})
            else:
                result.append({'lat': lat, 'long': lon})
            response.extend(result)

    with open(output_path, "w") as f:
        json.dump(response, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    reverse_geocode_address()
