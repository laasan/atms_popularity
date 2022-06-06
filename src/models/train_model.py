import os
import click
import json
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor, Pool
from dotenv import load_dotenv

load_dotenv()
remote_server_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(remote_server_uri)

CAT_FEATURES = [
    # "atm_group",
    "geo_city"
]


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def train(input_paths: list[str], output_path: str):
    with mlflow.start_run():
        mlflow.get_artifact_uri()

        df = pd.read_csv(input_paths[0])
        df.set_index("id", inplace=True)
        y = df["target"]
        X = df.drop("target", axis=1)
        x_train, x_val, y_train, y_val = train_test_split(
            X, y, test_size=0.15, random_state=14
        )

        train_pool = Pool(x_train, y_train, cat_features=CAT_FEATURES)
        val_pool = Pool(x_val, y_val, cat_features=CAT_FEATURES)

        with open(input_paths[1]) as f:
            params = json.load(f)
        params.update(
            {
                "iterations": 800,
                # "eval_metric": "RMSE",
                "random_seed": 14,
                "custom_metric": ["MAE", "RMSE"],
            }
        )

        model = CatBoostRegressor(**params)
        model.fit(train_pool, eval_set=val_pool, verbose=100)
        score = model.get_best_score()["validation"]
        model.save_model(output_path)

        mlflow.log_params(params)
        mlflow.log_metrics(score)
        mlflow.catboost.log_model(
            cb_model=model,
            artifact_path="model",
            registered_model_name="atms_popularity_catboost")


if __name__ == "__main__":
    train()
