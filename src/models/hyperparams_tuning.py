import catboost
import click
import json
import optuna
import pandas as pd
from catboost.utils import eval_metric
from optuna.samplers import TPESampler
from sklearn.model_selection import train_test_split

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


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def hyperparams_tuning(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    df.set_index("id", inplace=True)
    df["atm_group"] = df["atm_group"].apply(str)

    x_train, x_val, y_train, y_val = train_test_split(
        df[FEATURES + CAT_FEATURES], df["target"], test_size=0.2, random_state=14
    )
    train_pool = catboost.Pool(x_train, y_train, cat_features=CAT_FEATURES)
    val_pool = catboost.Pool(x_val, y_val, cat_features=CAT_FEATURES)

    def objective(trial):
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
            "depth": trial.suggest_int("depth", 3, 10),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 10),
            "boosting_type": trial.suggest_categorical(
                "boosting_type", ["Ordered", "Plain"]
            ),
            "max_ctr_complexity": trial.suggest_int("max_ctr_complexity", 0, 8),
        }

        model = catboost.CatBoostRegressor(**params, random_seed=14)
        model.fit(train_pool, verbose=0, eval_set=val_pool)
        y_pred = model.predict(val_pool)
        return eval_metric(val_pool.get_label(), y_pred, "RMSE")

    sampler = TPESampler(seed=123)
    study = optuna.create_study(direction="maximize", sampler=sampler)
    study.optimize(objective, n_trials=20)

    print(study.best_params)
    with open(output_path, "w") as f:
        json.dump(study.best_params, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    hyperparams_tuning()
