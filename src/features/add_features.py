import click
import geopandas as gpd
import pandas as pd


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=3)
@click.argument("output_path", type=click.Path())
def add_features(input_paths: str, output_path: str):
    """Function adds features to the main DataFrame
    :param input_paths: Path to read main DataFrame and features data
    :param output_path: Path to save main DataFrame
    :return:
    """
    df = gpd.read_file(input_paths[0])
    pois = pd.read_csv(input_paths[1])
    nearest_atm_dist = pd.read_csv(input_paths[2])

    df = df.merge(pois, how="left", on="id")
    df["pois_cnt"] = df.loc[:, "atm":"veterinary"].sum(axis=1)
    df = df.merge(nearest_atm_dist, how="left", on="id")

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    add_features()
