# STUDENT: Jamie Huang 001195694
from Distances import load_distances, calculate_distance, plan_route
from Time import convert_time, add_minutes, display_time


def load_delivery(package_table, index, delivery_time, truck_array):
    # O(1)
    # Auto update delayed packages if arrival time has passed
    if (convert_time('9:05') <= convert_time(delivery_time)) and len(package_table.delayed_packages) > 0:
        print('Delayed packages have arrived at the hub: {}'.format(package_table.delayed_packages))
        print()
        delayed_length = len(package_table.delayed_packages)
        # O(N) - 4 delayed packages
        for i in range(0, delayed_length):
            package = package_table.delayed_packages[0]
            package_table.search(int(package)).status = 'Ready for Delivery'
            package_table.delayed_packages.remove(int(package_table.search(int(package)).id))
            package_table.ready.append(int(package_table.search(int(package)).id))


    # O(1)
    # Auto correct wrong address for visualization purposes
    if convert_time('10:20') <= convert_time(delivery_time):
        print('Wrong address for package #9 corrected at 10:20 AM')
        corrected_package = 9
        package_table.search(corrected_package).address = '410 S State St'
        package_table.search(corrected_package).zip = '84111'
        package_table.search(corrected_package).status = 'Ready for Delivery'
        package_table.search(corrected_package).truck = None
        # Update status in package table lists as appropriate
        package_table.address_array[corrected_package - 1] = '410 S State St'
        if int(corrected_package) in package_table.wrong_address:
            package_table.wrong_address.remove(int(corrected_package))
            package_table.ready.append(int(corrected_package))
        # 410 S State St., Salt Lake City, UT 84111

    addresses = []
    address_multiple = []
    truck = None
    # Find first available truck at delivery time to load new packages in
    # O(N) - 3 available trucks
    for available_truck in truck_array:
        if available_truck.current_time is None or (available_truck.current_time is not None and available_truck.current_time < convert_time(delivery_time)):
            if truck is None:
                truck = available_truck
    delayed_packages = package_table.delayed_packages
    delivered = package_table.delivered
    address_array = list(set(package_table.address_array).difference(set(package_table.wrong_address)))
    early_delivery_ready = set(package_table.early_delivery).difference(set(delayed_packages)).difference(set(package_table.wrong_address))
    required_trucks = package_table.required_trucks
    grouped_packages = package_table.grouped_packages

    # load priority
    if index != 1:
        required_truck = required_trucks[index]

        # load packages that must be on current truck
        # O(N) - # of items required to be on specific truck
        if len(required_truck) > 0:
            for item in range(0, len(required_truck)):
                package_result = package_table.search(int(required_truck[item]))
                truck.load(package_result, delivery_time)
                if package_result.truck is None:
                    package_result.truck = truck
                    addresses.append(package_result.address)

        # Add packages with early delivery requirements on truck
        # O(N) - # of items with early delivery deadlines
        if len(early_delivery_ready) > 0:
            for item in early_delivery_ready:
                package_result = package_table.search(int(item))
                if package_result.truck is None:
                    truck.load(package_result, delivery_time)
                    package_result.truck = truck
                    addresses.append(package_result.address)

        # If any grouped packages are in the early loaded list, also add the other grouped packages to truck
        # O(N^2) - if an early delivery item in a group, check each item in each group package to put relevant packages on truck
        if len(grouped_packages) > 0:
            for grouped_package in grouped_packages:
                if bool(set(early_delivery_ready) & set(grouped_package)):
                    for item in grouped_package:
                        if item not in early_delivery_ready:
                            package_result = package_table.search(int(item))
                            truck.load(package_result, delivery_time)
                            package_result.truck = truck
                            addresses.append(package_result.address)

        # Check if any of the addresses already on the delivery list have other packages ready for delivery
        # O(N) - # of addresses packages are being delivered to
        for i in range(1, len(addresses)):
            if address_array.count(addresses[i]) > 1:
                address_multiple.append(i)

        # load packages for addresses that have multiple packages, to minimize the list of addresses needed later on
        if not truck.is_full():
            # O(N^2)
            for i in range(0, len(address_multiple)):
                multiple_package = package_table.search(address_multiple[i])
                # Load packages for addresses on delivery list until all packages for a given address is loaded
                if multiple_package is not None and addresses.count(multiple_package.address) < address_array.count(
                        multiple_package.address):
                    for j in range(1, package_table.length + 1):
                        same_address = package_table.search(j)
                        if same_address.address == multiple_package.address and same_address.truck is None and not truck.is_full():
                            if same_address.required_truck is None or (
                                    same_address.required_truck is not None and same_address.required_truck == truck.id):
                                truck.load(same_address, delivery_time)
                                same_address.truck = truck
                                addresses.append(same_address.address)

        if not truck.is_full():
            # Load the rest of the packages if no more prioritized packages exist
            ready = len(package_table.ready)
            # O(N) - Number of packages ready
            for i in range(0, ready):
                package_result = package_table.search(int(package_table.ready[i]))
                if package_result.truck is None and not truck.is_full():
                    truck.load(package_result, delivery_time)
                    package_result.truck = truck

    elif index == 1:
        required_truck = required_trucks[index]

        # For the 2nd truck, keep the load minimal with urgent packages
        # so delayed early delivery packages don't miss deadline

        # Add packages with early delivery requirements on truck
        for item in early_delivery_ready:
            package_result = package_table.search(int(item))
            if package_result.truck is None:
                truck.load(package_result, delivery_time)
                package_result.truck = truck
                addresses.append(package_result.address)

        # If any grouped packages are in the early loaded list, also add the other grouped packages to truck
        # O(N^2)
        for grouped_package in grouped_packages:
            if bool(set(early_delivery_ready) & set(grouped_package)):
                for item in grouped_package:
                    if item not in early_delivery_ready:
                        package_result = package_table.search(int(item))
                        truck.load(package_result, delivery_time)
                        package_result.truck = truck
                        addresses.append(package_result.address)

        # Load any packages required to be on truck
        if len(required_truck) > 0:
            for item in range(0, len(required_truck)):
                package_result = package_table.search(int(required_truck[item]))
                truck.load(package_result, delivery_time)
                if package_result.truck is None:
                    package_result.truck = truck
                    addresses.append(package_result.address)

        # Load the list of delivered addresses
        for item in delivered:
            package_result = package_table.search(int(item))
            addresses.append(package_result.address)

        # Check if any of the addresses already on the delivery list have other packages ready for delivery
        for i in range(1, len(addresses)):
            if address_array.count(addresses[i]) > 1:
                address_multiple.append(i)

        for i in range(0, len(address_multiple) - 1):
            multiple_package = package_table.search(address_multiple[i])
            # Load packages for addresses on delivery list until all packages for a given address is loaded
            if multiple_package is not None and addresses.count(multiple_package.address) < address_array.count(multiple_package.address):
                for j in range(1, package_table.length + 1):
                    same_address = package_table.search(j)
                    if same_address.address == multiple_package.address and same_address.truck is None and not truck.is_full():
                        truck.load(same_address, delivery_time)
                        same_address.truck = truck
                        addresses.append(same_address.address)

        # make a list of addresses with multiple packages ready for delivery
        mult_address_array = []
        for i in range(1, package_table.length + 1):
            multiple_package = package_table.search(i)
            if multiple_package.address not in mult_address_array:
                if address_array.count(multiple_package.address) > 1:
                    mult_address_array.append(multiple_package.address)
                    address_multiple.append(i)

        # Continue loading packages to deliver to addresses that have multiple packages ready for delivery
        # O(N^2)

        for k in range(0, len(address_multiple)):
            multiple_package = package_table.search(address_multiple[k])
            if multiple_package is not None and not truck.is_full():
                # O(N) - number of addresses with more than one package
                while not truck.is_full() and (addresses.count(multiple_package.address) < address_array.count(multiple_package.address)):
                    # O(N) - check
                    for j in range(1, package_table.length + 1):
                        same_address = package_table.search(j)
                        if same_address.address == multiple_package.address and same_address.truck is None and not truck.is_full():
                            truck.load(same_address, delivery_time)
                            same_address.truck = truck
                            addresses.append(same_address.address)

        if not truck.is_full():
            # Load the rest of the packages if no more prioritized packages exist
            ready = len(package_table.ready)
            # O(N) - Number of packages ready
            for i in range(0, 4):
                package_result = package_table.search(int(package_table.ready[i]))
                if package_result.truck is None and not truck.is_full():
                    truck.load(package_result, delivery_time)
                    package_result.truck = truck

    print('Truck {}: {} packages'.format(truck.id, str(len(truck.packages))))

    return truck


# TRUCKS
#   Carry 16 packages max
#   Drive at 18 mi/hr average
#   Infinite gas and no need to stop

class Truck:
    def __init__(self, id):
        self.id = id
        self.avg_mph = 18.0
        self.max_load = 16
        self.packages = []
        self.status = 'At Hub'
        self.start_loc = 'Hub'
        self.current_loc = 'Hub'
        self.route = []
        self.route_distance = 0.0
        self.traveled = 0.0
        self.current_time = None

    # Check if truck is full
    def is_full(self):
        return len(self.packages) == self.max_load

    def load(self, package, depart_time):
        # Reject new packages that are on other trucks, not ready, or when the current truck is full
        # O(1)
        if self.is_full() or package.status != 'Ready for Delivery' or package.truck is not None:
            return False
        if package.required_truck is not None and package.required_truck != self.id:
            return False
        self.packages.append(package)

        if package.address not in self.route:
            # O(N^2) - greedy closest distance/route planning
            self.route = plan_route(self.packages)[0]
            self.route_distance = plan_route(self.packages)[1]
        return True

    def run_delivery(self, depart_time, current_time, package_table):
        distance_list = load_distances()
        self.traveled = 0
        self.route_distance = 0
        self.current_time = convert_time(depart_time)
        self.status = 'Out for Delivery'
        # set packages to out for delivery
        # O(N) - # of packages on truck, max 16
        for i in range(0, len(self.packages)):
            package = package_table.search(self.packages[i].id)
            package_table.ready.remove(int(package.id))
            package_table.trucks[package.truck.id - 1].append(int(package.id))
            package.status = 'Out for Delivery'

        self.route.append(2)
        # Use greedy algorithm to find matching packages on delivery
        # O(N^2) - # of addresses on route, max 17 (16 unique addresses and trip back to hub)
        for i in range(0, len(self.route) - 1):
            current = self.route[i]
            next = self.route[i + 1]
            distance = calculate_distance(current, next)
            minutes = (distance / self.avg_mph) * 60.0
            # Check if there is time to start delivery
            if add_minutes(self.current_time, minutes) < convert_time(current_time):
                self.current_loc = next
                self.traveled = round(self.traveled + distance, 2)
                self.current_time = add_minutes(self.current_time, minutes)
                # O(N) - # of packages on truck for delivery
                for package in self.packages:
                    # Display 1st line of current address name
                    current_loc = distance_list[self.current_loc - 1][0].splitlines()[1].strip()
                    # Check if package may be delivered to current location
                    # and if there is enough time to make it to the next location
                    if (current_loc == package.address):
                        # Once destination is reached, remove package from special delivery lists if applicable
                        if package.id in package_table.early_delivery:
                            package_table.early_delivery.remove(package.id)
                        if package.id in package_table.wrong_address:
                            package_table.wrong_address.remove(package.id)
                        if package.id in package_table.delayed_packages:
                            package_table.delayed_packages.remove(package.id)
                        package_table.trucks[package.truck.id - 1].remove(int(package.id))

                        # Log package as delivered
                        package_table.delivered.append(int(package.id))
                        package.delivered_at = add_minutes(self.current_time, minutes)
                        package_table.address_array[int(package.id) - 1] = ''
                        package.status = 'Delivered'
                        deadline = ''
                        # Show deadline and delivery completion information
                        if package.deadline != 'EOD':
                            deadline = package.deadline
                        if deadline != '' and deadline != 'EOD':
                            deadline = ' || Deadline {}'.format(deadline)
                        print('     {} || package {} delivered to {}{} '.format(display_time(package.delivered_at), package.id, package.address, deadline))
        # Display completed trip info
        if self.current_time < convert_time(current_time):
            # Return truck to hub
            print('Trip Distance: {} miles'.format(self.traveled))
            print('Trip Completion Time: {}'.format(display_time(self.current_time)))
            print()
            self.status = 'At Hub'
            self.packages = []
            self.route = []
        return [self.traveled, self.current_time]
