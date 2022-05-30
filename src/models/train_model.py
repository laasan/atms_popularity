import click
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

mlflow.set_experiment('catboost')


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def train(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    df.set_index("id", inplace=True)
    df["atm_group"] = df["atm_group"].apply(str)

    x_train, x_val, y_train, y_val = train_test_split(
        df[FEATURES + CAT_FEATURES], df["target"], test_size=0.2, random_state=14
    )

    train_pool = Pool(x_train, y_train, cat_features=CAT_FEATURES)
    val_pool = Pool(x_val, y_val, cat_features=CAT_FEATURES)

    params = {
        "iterations": 500,
        "learning_rate": 0.1,
        "eval_metric": "RMSE",
        "depth": 4,
        "l2_leaf_reg": 2,
        "random_seed": 14,
        'custom_metric': ['MAE', 'RMSE']
    }
    mlflow.log_params(params)

    model = CatBoostRegressor(**params)
    model.fit(train_pool, eval_set=val_pool, verbose=100)
    score = model.get_best_score()['validation']
    model.save_model(output_path)

    mlflow.log_metrics(score)
    mlflow.log_artifact(output_path)


if __name__ == "__main__":
    train()
