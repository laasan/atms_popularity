import pandas as pd
from dadata import Dadata


enriched_data = pd.DataFrame()
df = pd.read_csv("data/interim/find_gaps.csv", index_col=0)
token = "08e834c01c8911fb1b6b094f693320dd9384f64f"
secret = "78ddd9aa20281d96f879bc7e3394596bc23fb88c"
# dadata = Dadata(token, secret)
test_rows = df[:3]
# with Dadata(token, secret) as dadata:
#     for x in test_rows['address']:
#         response = dadata.clean(name="address", source=x)
#         response = pd.DataFrame.from_dict([response])
#         enriched_data = pd.concat([enriched_data, response])
# enriched_data.to_csv('data/interim/geocoded_data.csv')
