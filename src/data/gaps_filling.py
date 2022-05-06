import click
import pandas as pd


@click.command()
@click.argument("geocoded_data", type=click.Path(exists=True))
@click.argument("find_gaps", type=click.Path(exists=True))
@click.argument("enrichment_data_output_path", type=click.Path())
@click.argument("manual_check_data_output_path", type=click.Path())
def gaps_filling(
    geocoded_data: str,
    find_gaps: str,
    enrichment_data_output_path: str,
    manual_check_data_output_path: str,
):
    """Function adds coordinates of points that were successfully geocoded to the main DataFrame
    :param geocoded_data: Path to read main DataFrame
    :param find_gaps: Path to read DataFrame with geocoded gaps
    :param enrichment_data_output_path: Path to save enrichment DataFrame
    :param manual_check_data_output_path: Path to save DataFrame for manual check
    :return:
    """
    combined_df = pd.read_csv(geocoded_data, index_col=0)
    geocoded_gaps = pd.read_csv(find_gaps)

    geocoded_gaps.drop("Unnamed: 0", axis=1, inplace=True)
    geocoded_gaps = geocoded_gaps[["source", "result", "geo_lat", "geo_lon", "qc_geo"]]
    geocoded_gaps = geocoded_gaps.drop_duplicates(subset=["source"])
    geocoded_gaps = geocoded_gaps[geocoded_gaps["qc_geo"] < 2]
    geocoded_gaps.rename(
        columns={"result": "address_rus", "geo_lat": "lat", "geo_lon": "long"},
        inplace=True,
    )
    geocoded_gaps.drop("qc_geo", axis=1, inplace=True)
    df = (
        combined_df.set_index("address")
        .combine_first(geocoded_gaps.set_index("source"))
        .reset_index()
    )
    df.rename(columns={"index": "address"}, inplace=True)

    df[df["address_rus"].notnull()].to_csv(enrichment_data_output_path, index=False)
    df[df["address_rus"].isnull()].to_csv(manual_check_data_output_path, index=False)


if __name__ == "__main__":
    gaps_filling()
