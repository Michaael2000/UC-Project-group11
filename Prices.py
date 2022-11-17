from datetime import datetime as dt
import pandas as pd

df = pd.read_csv("df_july.csv")
# df_july = df[df['TIMESTAMP'] <= 1375307999]
# df_july.to_csv("data/df_july.csv")

# timestamps_july = df_july['TIMESTAMP']
# dates_july = timestamps_july.apply(dt.fromtimestamp)

print(df)
temp_df = pd.DataFrame()
temp_df = pd.concat([temp_df, df.loc[df['POLYLINE'].str.len() < 55]], axis=0)
df = pd.concat([df, temp_df], axis=0).drop_duplicates(keep=False)
df.to_csv("data/df_july_clean.csv")
print(df)

