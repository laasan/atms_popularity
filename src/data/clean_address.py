import click
import json
import pandas as pd


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_paths", type=click.Path(), nargs=2)
@click.argument("qc_geo", type=click.INT)
def clean_address(input_paths: list[str], output_paths: list[str], qc_geo: int):
    """The function merges raw data and geocoding results
    :param input_paths: Paths to read combined DataFrame and geocoded addresses
    :param output_paths: Paths to save DataFrame with high coordinate accuracy
                        and data for manual address checking
    :param qc_geo: Address coordinate accuracy
    :return:
    """
    combined_df = pd.read_csv(input_paths[0])
    with open(input_paths[1], "r") as f:
        geocoded_addresses = json.load(f)
    geocoded_addresses = pd.json_normalize(geocoded_addresses)

    df = pd.merge(
        combined_df[["id", "atm_group", "address", "target", "is_train"]],
        geocoded_addresses[["source", "result", "geo_lat", "geo_lon", "qc_geo"]],
        how="left",
        left_on="address",
        right_on="source",
    )
    manual_check_data = df[df["qc_geo"] > qc_geo].drop("source", axis=1)
    df = df[df["qc_geo"] <= qc_geo]
    df.drop(["source", "qc_geo"], axis=1, inplace=True)
    df.rename(columns={"result": "address_rus"}, inplace=True)
    df = df[
        [
            "id",
            "atm_group",
            "address",
            "address_rus",
            "geo_lat",
            "geo_lon",
            "target",
            "is_train",
        ]
    ]

    df.to_csv(output_paths[0], index=False)
    manual_check_data.to_csv(output_paths[1], index=False)


if __name__ == "__main__":
    clean_address()
