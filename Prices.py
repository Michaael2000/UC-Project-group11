from datetime import datetime as dt
import pandas as pd

df = pd.read_csv("df_july.csv")
df_2 = pd.DataFrame()
print(len(df_2))
# df_july = df[df['TIMESTAMP'] <= 1375307999]
# df_july.to_csv("df_july.csv")

# timestamps_july = df_july['TIMESTAMP']


# dates_july = timestamps_july.apply(dt.fromtimestamp)
# print(dates_july.head())
outliers = []
for i in range(len(df['POLYLINE'])):
    if len(df['POLYLINE'][i]) < 55:
        outliers.append(i)
        df_2 = pd.concat([df_2, ])
print(len(outliers))
df.drop(outliers, axis=0, inplace=True)

# print(df[0])
