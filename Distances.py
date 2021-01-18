# STUDENT: Jamie Huang 001195694
import csv


# O(1)
def load_distances():
    with open('./data/wgups_distance.csv') as distance_csv:
        # load package csv data into list
        read_distance = csv.reader(distance_csv, delimiter=',')
        distance_list = list(read_distance)
    return distance_list


# O(1) - Get location name from index
def get_name_from_index(index):
    distance_list = load_distances()
    return distance_list[index - 1][0].splitlines()[0].strip()


# O(1) - Get first address line, not location name
def get_address_from_index(index):
    distance_list = load_distances()
    return distance_list[index - 1][0].splitlines()[1].strip()


# Get index of given address to find info in distance list
# O(N) - max 28 addresses
def get_address_index(address):
    distance_list = load_distances()
    address_column = 0
    # search for address in the first row of the distance CSV
    # O(N)
    for j in range(1, len(distance_list) + 1):
        if address in distance_list[0][j]:
            address_column = j
    # Return error if address is not found in first row
    if address_column == 0:
        print("Cannot find: "+address)
    return address_column


# O(1)
# Search for distance between two points when given address indexes
def calculate_distance(address_1, address_2):
    distance_list = load_distances()
    index_1 = address_1
    index_2 = address_2
    if address_1 < address_2:
        index_1 = address_2
        index_2 = address_1
    distance = float(distance_list[index_1 - 1][index_2])
    return distance


# O(1)
# Search for distance between two points when given address strings
def get_distance(address_1, address_2):
    distance_list = load_distances()
    index_1 = get_address_index(address_1)
    index_2 = get_address_index(address_2)
    if index_1 < index_2:
        index_1 = get_address_index(address_2)
        index_2 = get_address_index(address_1)
    distance = float(distance_list[index_1 - 1][index_2])
    return distance


# O(N^2)
# Plan optimal route to and from hub to all delivery locations when given package list
def plan_route(packages):
    distance_list = load_distances()
    index_array = []
    path = []
    total_distance = 0
    shortest_distance = float("inf")

    # make address array from packages
    # O(N) - max 16 packages
    for i in range(0, len(packages)):
        delivery_package = packages[i]
        # Only add unique addresses to array
        address_index = get_address_index(delivery_package.address)
        if address_index not in index_array:
            index_array.append(address_index)

    # O(nlogn) time complexity, O(n) space complexity - Timsort sorting method
    index_array.sort()

    # Add hub as the starting location for trip
    index_array.insert(0, 2)
    current_address = index_array[0]
    # Loop through each location and find the shortest distance to the next point, starting from the hub
    # O(N^2) - max 16 addresses on truck
    for j in range(0, len(index_array)):
        shortest_distance = float("inf")
        for i in range(0, len(index_array)):
            address_1 = current_address
            address_2 = index_array[i]
            if address_1 < address_2:
                address_1 = index_array[i]
                address_2 = current_address
            distance = float(distance_list[address_1 - 1][address_2])
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_path = index_array[i]
        # Remove visited locations from our list of addresses to visit
        if shortest_path in index_array:
            index_array.remove(shortest_path)
        # Move truck to the shortest path location
        path.append(shortest_path)
        total_distance += shortest_distance
        current_address = shortest_path

    # After all packages are delivered, calculate path back to hub and add to trip distance
    address_1 = current_address
    address_2 = 2
    if address_1 < address_2:
        address_1 = 2
        address_2 = current_address
    distance = float(distance_list[address_1 - 1][address_2])
    total_distance += distance
    return [path, total_distance]
