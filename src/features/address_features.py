import click
import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def address_features(input_path: str, output_path: str):
    """Function generates features based on the ATM address
    :param input_path: Path to read main DataFrame
    :param output_path: Path to save address features
    :return:
    """
    df = pd.read_csv(input_path)

    df = pd.merge(
        df,
        df.groupby("address_rus", as_index=False).agg(atm_cnt_adrs=("id", "count")),
        how="left",
        on="address_rus",
    )
    df = pd.merge(
        df,
        df.groupby("geo_city", as_index=False).agg(atm_cnt_city=("id", "count")),
        how="left",
        on="geo_city",
    )
    df = pd.merge(
        df,
        df.groupby(["geo_city", "atm_group"], as_index=False).agg(
            atmgroup_cnt_city=("id", "count")
        ),
        how="left",
        on=["geo_city", "atm_group"],
    )
    df["atmgroup_share_city"] = df["atmgroup_cnt_city"] / df["atm_cnt_city"]
    df = df[
        [
            "id",
            "atm_cnt_adrs",
            "atm_cnt_city",
            "atmgroup_cnt_city",
            "atmgroup_share_city",
        ]
    ]

    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    address_features()
