import click
import pandas as pd


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def find_gaps(input_path: str, output_path: str):
    """Function selects rows with missing values into a separate data set
    :param input_path: Path to read combined DataFrame
    :param output_path: Path to save DataFrame with missing values
    :return:
    """
    df = pd.read_csv(input_path, index_col=0)

    df = df[df["address_rus"].isnull()]

    df.to_csv(output_path)


if __name__ == "__main__":
    find_gaps()
