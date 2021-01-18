# STUDENT: Jamie Huang 001195694
import csv
from HashTable import PackageTable
from Time import display_time

# PACKAGE
#   Up to one special note per package
#   May have wrong delivery address, corrected at 10:20am for package 9
#   ID is unique
# 40 packages per day


class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, note, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status
        self.truck = None
        self.required_truck = None
        self.left_hub = None
        self.delivered_at = None

    def print(self):
        print()
        print('PACKAGE ID: ' + self.id)
        print('ADDRESS: ' + self.address + ', ' + self.city + ', ' + self.state + ' ' + self.zip)
        print('DELIVERY DEADLINE: ' + self.deadline)
        if self.delivered_at is not None:
            print('DELIVERED AT: ' + display_time(self.delivered_at))
        print('PACKAGE WEIGHT: ' + self.weight)
        print('NOTE: ' + self.note)
        print('STATUS: ' + self.status)


def load_packages():
    with open('./data/wgups_packages.csv') as package_csv:
        # load package csv data into hash table, skipping header row of addresses
        read_csv = csv.reader(package_csv, delimiter=',')
        next(read_csv)
        package_table = PackageTable()
        # Parse csv row data and create package from info
        # O(N) - 40 package rows
        for row in read_csv:
            id_row = row[0]
            address_row = row[1]
            city_row = row[2]
            state_row = row[3]
            zip_row = row[4]
            delivery_row = row[5]
            size_row = row[6]
            note_row = row[7]
            # Add custom statuses for delayed/wrong address notes
            if 'Delayed on flight' in note_row:
                status_row = 'Delayed on flight'
            elif 'Wrong address' in note_row:
                status_row = 'Awaiting address correction'
            else:
                status_row = 'Ready for Delivery'
            package = Package(id_row, address_row, city_row, state_row, zip_row, delivery_row, size_row, note_row, status_row)
            package_table.insert(int(package.id), package)
    return package_table