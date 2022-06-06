import requests
import pandas as pd

test_df = pd.read_csv("data/processed/train.csv")
test_df.set_index("id", inplace=True)
test_df = test_df.drop("target", axis=1)
x_holdout = test_df.iloc[0:3]

headers = {"Content-Type": "application/json"}
response = requests.post("http://127.0.0.1:5003/invocations",
                         data=x_holdout.to_json(orient="split"),
                         headers=headers)

print(response.content)
