import ast
import math
import datetime
import numpy as np
import pandas as pd
import geopandas as gpd


price_range = 0.5
standard_price = 0.47
max_price = standard_price * (1 + price_range)
max_p_sqrd = math.pow(max_price, 2)


# Cumulative Distribution Function (Fw & Fr)
def F(price):
    return math.pow(price, 2) / math.pow(max_price, 2)


# Demand
def D(r, price):
    return r * (1 - F(price))


def Dinv(r, demand):
    return math.sqrt(max_p_sqrd*(1 - (demand / r)))


# Supply
def S(v, price):
    return v * F(price)


def T(r, v, p):
    return min(D(r, p), S(v, p))


def three_closest_points(loc_coord, polylines, timestamps, origin):
    nr_entries = 20038
    R_V = []
    coord_list = [(x, y) for x, y in zip(loc_coord.x, loc_coord.y)]
    demand = [0] * len(coord_list)
    previous_t = 0
    for i in range(0, nr_entries):

        current_timestamp = timestamps[i]
        current_t = current_timestamp.hour
        if current_t > previous_t:
            R_V.append(demand)
            demand = [0] * len(coord_list)

        distances = [0] * len(coord_list)
        if origin:
            coords = (polylines[i][0][0], polylines[i][0][1])
        else:
            coords = (polylines[i][-1][0], polylines[i][-1][1])

        for j in range(len(coord_list)):
            distances[j] = math.dist(coords, coord_list[j])

        top_three = np.argsort(distances)[:3]
        demand[top_three[0]] += 1
        demand[top_three[1]] += 1
        demand[top_three[2]] += 1
        previous_t = current_t
    return R_V


def actualRV():
    dists = pd.read_csv('distances.txt', sep="\n", header=None)
    dists.columns = ["DISTANCE"]
    df_july_firstweek = pd.read_csv('df_july_firstweek_short.csv')
    df_july_firstweek["DISTANCE"] = dists["DISTANCE"]
    df_july_firstweek["TIMESTAMP"] = df_july_firstweek["TIMESTAMP"].apply(datetime.datetime.fromtimestamp)
    df_july_firstweek.sort_values(by=['TIMESTAMP'], ignore_index=True, inplace=True)
    polylines = df_july_firstweek['POLYLINE'].apply(ast.literal_eval)
    timestamps = df_july_firstweek['TIMESTAMP']

    shapefile_df = gpd.read_file("Shapefile/places.shp")
    loc_coord = shapefile_df["geometry"]
    Rti = three_closest_points(loc_coord, polylines, timestamps, True)
    Vj = three_closest_points(loc_coord, polylines, timestamps, False)
    return Rti, Vj


def revIncrease(r, v, r1, v1):
    pc = calculateClearingPrice(r, v)
    pc1 = calculateClearingPrice(r1, v1)
    return S(v1, pc1) * pc1 - S(v, pc) * pc


def calculateClearingPrice(r, v):
    return math.sqrt((r * max_p_sqrd) / (v + r))


def localOptimization(r, v):
    clearingPrice = calculateClearingPrice(r, v)  # Pc D(p) = S(p)
    maxDemandPrice = math.sqrt(max_p_sqrd / 3)  # Maximizes D(p) * p -> Pd
    # print("Pd", maxDemandPrice)
    # print("Pc", clearingPrice)

    if maxDemandPrice <= clearingPrice:
        return clearingPrice
    else:
        return maxDemandPrice


def revDecrease(r, pti):
    price_change = (pti - standard_price) / standard_price
    adjusted_r = r + price_change * r
    revdecrease = r * standard_price - pti * adjusted_r
    return revdecrease, adjusted_r


def PPricing(t, r, v):
    """
    Input: Rti, Vti & R(t+1)j
    Output: p*ti, optimal price at time t
    """
    revDec = []
    adjusted_rs = []
    revInc = []
    n = 533
    for i in range(n):
        if r[t][i] == 0 and v[t][i] == 0:
            revDec.append(0)
            adjusted_rs.append(0)
            continue
        pti = localOptimization(r[t][i], v[t][i])
        res1, res2 = revDecrease(r[t][i], pti)
        revDec.append(res1)
        adjusted_rs.append(res2)
    for j in range(n):
        if adjusted_rs[j] == 0 and v[t][j] == 0 or r[t + 1][j] == 0 and v[t + 1][j] == 0:
            revInc.append(0)
            continue
        revInc.append(revIncrease(adjusted_rs[j], v[t][j], r[t + 1][j], v[t + 1][j]))

    sigmaInc = sum(revInc)
    sigmaDec = sum(revDec)
    return sigmaInc - sigmaDec


if __name__ == "__main__":
    r, v = actualRV()
    l = []
    for t in range(1, 99):
        l.append(PPricing(t, r, v))
    print(sum(l))

