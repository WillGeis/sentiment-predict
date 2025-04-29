import pandas as pd

# Load the CSV
df = pd.read_csv("master_stocks.csv")

df_no_timestamp = df.drop(columns=["timestamp"])

df_no_timestamp.to_csv("master_stocks.csv", index=False)