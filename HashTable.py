# STUDENT: Jamie Huang 001195694
# HashTable class using chaining.
import re


def print_status_packages(status_list, package_table):
    # O(N^2)
    # O(N) - # of packages in status list
    for i in range(0, len(status_list)):
        # Search for desired package after running delivery
        # O(N) - # of packages in unique bucket being searched
        package_result = package_table.search(int(status_list[i]))

        # Display formatted package information
        # O(1)
        if package_result is None:
            print()
            print("No package found")
        else:
            package_result.print()


class PackageTable:
    # Set capacity near expected package count for minimal perfect hashing
    # O(N) - initial capacity
    def __init__(self, initial_capacity=40):
        self.table = []
        self.length = 0
        for i in range(initial_capacity):
            self.table.append([])
        self.early_delivery = []
        self.ready = []
        self.wrong_address = []
        self.delayed_packages = []
        self.trucks = [[], [], []]
        self.required_trucks = [[], [], []]
        self.delivered = []
        self.grouped_packages = []
        self.package_count = 0
        self.address_array = []

    # O(1)
    def get_hash(self, key):
        bucket = int(key) % len(self.table)
        return bucket

    # O(N^2)
    def insert(self, key, package):
        # Get the bucket list to put item into
        bucket = self.get_hash(key)
        bucket_list = self.table[bucket]
        self.length += 1
        # Insert item to the end of the bucket list
        bucket_list.append(package)
        package_id = int(package.id)
        delivery_deadline = package.deadline
        package_note = package.note
        self.address_array.append(package.address)
        self.package_count += 1
        # Check for special conditions and load package id to corresponding lists if applicable
        if delivery_deadline != 'EOD':
            self.early_delivery.append(package_id)
        if package.status == 'Ready for Delivery':
            self.ready.append(package_id)
        if "Delayed" in package_note:
            self.delayed_packages.append(package_id)
        if "Wrong address" in package_note:
            self.wrong_address.append(package_id)
        if "only be on truck" in package_note:
            match = re.findall(r"(\d+)", package_note)
            truck = self.required_trucks[int(str(match[0])) - 1]
            truck.append(package_id)
            package.required_truck = int(str(match[0]))
        if "Must be delivered with" in package_note:
            # Find package numbers current package must be grouped with
            match = re.findall(r"(\d+)", package_note)
            # Check if any packages in current package are already in a package group
            already_required = [package_id in (item for sublist in self.grouped_packages for item in sublist)]

            for required in match:
                shared_required = required in (item for sublist in self.grouped_packages for item in sublist)
                already_required.append(shared_required)

            # Build grouped package from current row
            # O(N^2)
            grouped_package = [package_id]
            for item in match:
                grouped_package.append(item)

            if True in already_required:
                for package_item in grouped_package:
                    for sublist in self.grouped_packages:
                        if package_item not in sublist:
                            sublist.append(package_item)
            else:
                self.grouped_packages.append(grouped_package)

    # Search for an item with matching key
    # O(N) in theory - in practice, O(1) due to lack of collisions in bucket
    def search(self, key):
        # Get bucket list where key would be
        key = int(key)
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Search for the key in bucket list
        for i in range(len(bucket_list)):
            if int(bucket_list[i].id) == key:
                # Find item's index and return item in bucket list
                return bucket_list[i]
        return None

    # Remove item with matching key from the hash table
    # O(1) under ideal conditions
    # O(N)
    def remove(self, key):
        # Get the bucket list where this item will be removed from
        bucket = hash(key) % len(self.table)
        self.length -= 1
        bucket_list = self.table[bucket]
        del self.address_array[key]
        # Remove item from the bucket list if it is present
        if key in bucket_list:
            bucket_list.remove(key)