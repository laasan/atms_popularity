import click
import pandas as pd

FEATURES = [
    "atm",
    "attraction",
    "bank",
    "bar",
    "bureau_de_change",
    "bus_station",
    "bus_stop",
    "cafe",
    "clinic",
    "college",
    "dentist",
    "fast_food",
    "fuel",
    "hospital",
    "hotel",
    "ice_cream",
    "marketplace",
    "office",
    "parking",
    "payment_terminal",
    "pharmacy",
    "photostudio",
    "post_office",
    "pub",
    "public_building",
    "restaurant",
    "shop",
    "theatre",
    "townhall",
    "train_station",
    "university",
    "veterinary",
    "pois_cnt",
    "near_atm_dist",
    # "atm_cnt_adrs",
    # "atm_cnt_city",
    # "atmgroup_cnt_city",
    # "atmgroup_share_city",
]
CAT_FEATURES = [
    # "atm_group",
    "geo_city"
]


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

    df = df.fillna(0)
    df.set_index("id", inplace=True)
    df["atm_group"] = df["atm_group"].apply(str)
    df = df[FEATURES + CAT_FEATURES + ["target"] + ["is_train"]]
    train_df = df[df["is_train"] == 1]
    train_df = train_df.drop(columns=["is_train"])
    test_df = df[df["is_train"] == 0]
    test_df = test_df.drop(columns=["is_train", "target"])

    train_df.to_csv(output_paths[0])
    test_df.to_csv(output_paths[1])


if __name__ == "__main__":
    prepare_data()
