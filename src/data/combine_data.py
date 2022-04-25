import pandas as pd
import click


@click.command()
@click.argument("train_path", type=click.Path(exists=True))
@click.argument("test_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def combine_data(train_path: str, test_path: str, output_path: str):
    """Function combines the training and test data sets
    :param train_path: Path to read original train DataFrame
    :param test_path: Path to read original test DataFrame
    :param output_path: Path to save combined DataFrame
    :return:
    """
    train_df = pd.read_csv(train_path, index_col=0)
    test_df = pd.read_csv(test_path, index_col=0)

    train_df["is_train"] = 1
    test_df["is_train"] = 0
    combined_df = pd.concat([train_df, test_df], sort=False)
    print("Train and test data are successfully combined.")

    combined_df.to_csv(output_path)


if __name__ == "__main__":
    combine_data()
