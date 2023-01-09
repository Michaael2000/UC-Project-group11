import pandas as pd
import ast


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


def assign_coordinates(n, divisionpoints, polylines, origin_or_destination):
    trips = [0] * (n * n)
    for i in range(20000):

        if origin_or_destination is True:
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

    return trips


df_july_firstweek = pd.read_csv('df_july_firstweek.csv')
polyline_july = df_july_firstweek['POLYLINE'].apply(ast.literal_eval)

division_points = create_grid(4)
origin_or_destination = True
demand = assign_coordinates(4, division_points, polyline_july, origin_or_destination)
print(demand)
