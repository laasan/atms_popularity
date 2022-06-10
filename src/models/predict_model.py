import requests
import pandas as pd

test_df = pd.read_csv("examples/test5.csv")
test_df.set_index("id", inplace=True)

host = '127.0.0.1'
port = '5001'

url = f'http://{host}:{port}/invocations'
headers = {'Content-Type': 'application/json'}
http_data = test_df.to_json(orient='split')

response = requests.post(url=url, headers=headers, data=http_data)

print(f'Predictions: {response.text}')
