import click
import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_paths", type=click.Path(), nargs=2)
def prepare_data(input_path: str, output_paths: list[str]):
    """
    Function splits data on training and test DataFrames
    and prepares the data for modeling
    :param input_path: Path to read DataFrame
    :param output_paths: Paths to save train and test Dataframes
    :return:
    """
    df = pd.read_csv(input_path)

    df.drop(
        columns=[
            "atm_group",
            "address",
            "address_rus",
            "geo_lat",
            "geo_lon",
            "geometry",
        ],
        inplace=True,
    )
    train_df = df[df["is_train"] == 1]
    train_df = train_df.drop(columns=["is_train"])
    test_df = df[df["is_train"] == 0]
    test_df = test_df.drop(columns=["is_train", "target"])

    train_df.to_csv(output_paths[0])
    test_df.to_csv(output_paths[1])


if __name__ == "__main__":
    prepare_data()
