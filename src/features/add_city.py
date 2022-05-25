import click
import json
import numpy as np
import pandas as pd

QC_GEO = 1


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def add_city(input_paths: list[str], output_path: str):
    """Function adds the city feature
    :param input_paths: Path to read cleaned DataFrame and geocoded addresses
    :param output_path: Path to save main DataFrame
    :return:
    """
    df = pd.read_csv(input_paths[0])
    with open(input_paths[1], "r") as f:
        geocoded_addresses = json.load(f)
    geocoded_addresses = pd.json_normalize(geocoded_addresses)

    geocoded_addresses = geocoded_addresses[geocoded_addresses["qc_geo"] <= QC_GEO]
    geocoded_addresses["geo_city"] = np.where(
        geocoded_addresses["city_with_type"].notnull(),
        geocoded_addresses["city_with_type"],
        geocoded_addresses["settlement_with_type"],
    )
    geocoded_addresses["geo_city"] = np.where(
        geocoded_addresses["geo_city"].isnull(),
        geocoded_addresses["area_with_type"],
        geocoded_addresses["geo_city"],
    )
    geocoded_addresses["geo_city"] = np.where(
        geocoded_addresses["geo_city"].isnull(),
        geocoded_addresses["region_with_type"],
        geocoded_addresses["geo_city"],
    )
    df = pd.merge(
        df,
        geocoded_addresses[["source", "geo_city"]].rename(
            columns={"source": "address"}
        ),
        how="left",
        on="address",
    )

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    add_city()
