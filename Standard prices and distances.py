from datetime import datetime as dt
import pandas as pd
import openrouteservice as ors
import ast
import time

# df = pd.read_csv("df_july.csv")
# df_july = df[df['TIMESTAMP'] <= 1375307999]
# df_july.to_csv("data/df_july.csv")

# timestamps_july = df_july['TIMESTAMP']
# dates_july = timestamps_july.apply(dt.fromtimestamp)

# temp_df = pd.DataFrame()
# temp_df = pd.concat([temp_df, df.loc[df['POLYLINE'].str.len() < 55]], axis=0)
# df = pd.concat([df, temp_df], axis=0).drop_duplicates(keep=False)
# df.to_csv("df_july_clean.csv")

# df_july = pd.read_csv('df_july_clean.csv')
# df_july_firstweek = df_july[df_july['TIMESTAMP'] <= 1373234399]
# df_july_firstweek.to_csv("df_july_firstweek.csv")

df_july_firstweek = pd.read_csv('df_july_firstweek.csv')
base_fee = 3.25
kilometer_fee = 0.47

def calculate_distances(polylines):
    client = ors.Client(key='5b3ce3597851110001cf62483353a6afa13243d3b8d665e5739e02ff')

    distances = []
    j = 0 #counter to limit API requests
    
    with open('distances.txt', 'a') as taxi:
        for i in range(1619, 5000):
            # start = time.time()
            start_coords = (polylines[i][0][0], polylines[i][0][1])
            end_coords = (polylines[i][-1][0], polylines[i][-1][1])
            coords = (start_coords, end_coords)
                
            route = client.directions(coords)
            # print(f"Program finished successfully in {time.time() - start} seconds")
            try:
                taxi.write(str(route['routes'][0]['summary']['distance']))
                taxi.write('\n')
            except KeyError:
                print(i)
            # distances.append(route['routes'][0]['summary']['distance'])
            j += 1
            # print(j)
            if j % 40 == 0: #sleep for 1 second after 40 API requests
                time.sleep(60)
#polylines [1323] moet nog
    # return distances

polyline_july = df_july_firstweek['POLYLINE'].apply(ast.literal_eval)

calculate_distances(polyline_july)

def price_calculator(distance, demand_factor):
    
    return base_fee + (kilometer_fee * demand_factor * distance)

# df_july_firstweek = df_july_firstweek.assign(Trip_distance=distances)
# df_july_firstweek.to_csv('july_firstweek_with_distances.csv')
