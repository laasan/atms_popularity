import requests
import pandas as pd


def atm_geo_popularity(df):
    test_df = df.set_index("id")

    host = "127.0.0.1"
    port = "5001"

    url = f"http://{host}:{port}/invocations"
    headers = {"Content-Type": "application/json"}
    http_data = test_df.to_json(orient="split")

    response = requests.post(url=url, headers=headers, data=http_data)
    result = pd.DataFrame(
        {"id": list(test_df.index), "popularity_idx": response.json()}
    )

    return result


if __name__ == "__main__":
    atm_geo_popularity()
