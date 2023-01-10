import ast
import math
import datetime
import pandas as pd

price_range = 0.5
standard_price = 0.47
max_price = standard_price * (1 + price_range)
max_p_sqrd = math.pow(max_price, 2)


def create_grid(n):
    top_left_coordinates_porto = (-8.724049960449397, 41.27097898784837)
    top_right_coordinates_porto = (-8.460677040139723, 41.27097898784837)
    bottom_left_coordinates_porto = (-8.724049960449397, 41.09871937936296)
    bottom_right_coordinates_porto = (-8.460677040139723, 41.09871937936296)

    divisionpoints = []

    # determine division points in the city, for a 4x4 grid we have four division points
    city_length = top_right_coordinates_porto[0] - top_left_coordinates_porto[0]
    city_height = top_left_coordinates_porto[1] - bottom_left_coordinates_porto[1]

    block_length = city_length / n
    block_height = city_height / n

    for i in range(n - 1):
        for j in range(n - 1):
            divisionpoint = (top_left_coordinates_porto[0] + block_length + block_length * i,
                             top_left_coordinates_porto[1] - block_height - block_height * j)
            divisionpoints.append(divisionpoint)

    return divisionpoints  # [top left, middle left, bottom left, top middle, middle middle, bottom middle, top right, middle right, bottom right]


def assign_coordinates(n, divisionpoints, polylines, timestamps, origin):
    trips = [0] * (n * n)
    res = []
    previous_t = 0
    for i in range(20038):
        current_timestamp = timestamps[i]
        current_t = current_timestamp.hour
        if current_t > previous_t:
            res.append(trips)
            trips = [0] * (n * n)

        if origin:
            coords = (polylines[i][0][0], polylines[i][0][1])
        else:
            coords = (polylines[i][-1][0], polylines[i][-1][1])
        # end_coords = (polylines[i][-1][0], polylines[i][-1][1])
        # coords = (start_coords, end_coords)
        first_coord_index_data_entry = coords[0]
        second_coord_index_data_entry = coords[1]

        # The first column of the grid
        if first_coord_index_data_entry < divisionpoints[0][0]:
            if second_coord_index_data_entry > divisionpoints[0][1]:
                trips[0] += 1
            elif second_coord_index_data_entry > divisionpoints[1][1]:
                trips[1] += 1
            elif second_coord_index_data_entry > divisionpoints[2][1]:
                trips[2] += 1
            else:
                trips[3] += 1

        # The second column of the grid
        elif first_coord_index_data_entry < divisionpoints[3][0]:
            if second_coord_index_data_entry > divisionpoints[3][1]:
                trips[4] += 1
            elif second_coord_index_data_entry > divisionpoints[4][1]:
                trips[5] += 1
            elif second_coord_index_data_entry > divisionpoints[5][1]:
                trips[6] += 1
            else:
                trips[7] += 1

        # The third column of the grid
        elif first_coord_index_data_entry < divisionpoints[6][0]:
            if second_coord_index_data_entry > divisionpoints[6][1]:
                trips[8] += 1
            elif second_coord_index_data_entry > divisionpoints[7][1]:
                trips[9] += 1
            elif second_coord_index_data_entry > divisionpoints[8][1]:
                trips[10] += 1
            else:
                trips[11] += 1

        # The fourth column of the grid
        else:
            if second_coord_index_data_entry > divisionpoints[6][1]:
                trips[12] += 1
            elif second_coord_index_data_entry > divisionpoints[7][1]:
                trips[13] += 1
            elif second_coord_index_data_entry > divisionpoints[8][1]:
                trips[14] += 1
            else:
                trips[15] += 1

        previous_t = current_t

    return res


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
    n = 16
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
    # dists = pd.read_csv('distances.txt', sep="\n", header=None)
    # dists.columns = ["DISTANCE"]
    df_july_firstweek = pd.read_csv('df_july_firstweek_short.csv')
    # df_july_firstweek["DISTANCE"] = dists["DISTANCE"]
    df_july_firstweek["TIMESTAMP"] = df_july_firstweek["TIMESTAMP"].apply(datetime.datetime.fromtimestamp)
    df_july_firstweek.sort_values(by=['TIMESTAMP'], ignore_index=True, inplace=True)
    polylines = df_july_firstweek['POLYLINE'].apply(ast.literal_eval)
    timestamps = df_july_firstweek['TIMESTAMP']
    data_points = 20038

    division_points = create_grid(4)
    demand = assign_coordinates(4, division_points, polylines, timestamps, True)
    supply = assign_coordinates(4, division_points, polylines, timestamps, False)
    l = []
    for t in range(1, 15):
        l.append(PPricing(t, demand, supply))
    print(sum(l))


