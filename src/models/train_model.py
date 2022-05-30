import click
import json
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor, Pool, metrics

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
    "atm_cnt_adrs",
    "atm_cnt_city",
    "atmgroup_cnt_city",
    "atmgroup_share_city",
]
CAT_FEATURES = ["atm_group", "geo_city"]

mlflow.set_experiment("catboost")


@click.command()
@click.argument("input_paths", type=click.Path(exists=True), nargs=2)
@click.argument("output_path", type=click.Path())
def train(input_paths: list[str], output_path: str):
    df = pd.read_csv(input_paths[0])
    df.set_index("id", inplace=True)
    df["atm_group"] = df["atm_group"].apply(str)

    x_train, x_val, y_train, y_val = train_test_split(
        df[FEATURES + CAT_FEATURES], df["target"], test_size=0.2, random_state=14
    )

    train_pool = Pool(x_train, y_train, cat_features=CAT_FEATURES)
    val_pool = Pool(x_val, y_val, cat_features=CAT_FEATURES)

    with open(input_paths[1]) as f:
        params = json.load(f)
    params.update({
        "iterations": 800,
        # "eval_metric": "RMSE",
        "random_seed": 14,
        "custom_metric": ["MAE", "RMSE"],
    })

    mlflow.log_params(params)

    model = CatBoostRegressor(**params)
    model.fit(train_pool, eval_set=val_pool, verbose=100)
    score = model.get_best_score()["validation"]
    model.save_model(output_path)

    mlflow.log_metrics(score)
    mlflow.log_artifact(output_path)


if __name__ == "__main__":
    train()
