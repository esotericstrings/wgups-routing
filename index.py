# STUDENT: Jamie Huang 001195694
from Package import load_packages
from Time import convert_time, display_time
from HashTable import print_status_packages
from Truck import load_delivery, Truck


def delivery(departure_times, truck_array):
    # Load package data from CSV and load trucks
    # O(N) - 40 package rows
    package_table = load_packages()

    delivery_time = input('Enter time to check delivery statuses: ')

    while (convert_time(delivery_time) is False) or not ((0 <= convert_time(delivery_time).hour < 24) and (0 <= convert_time(delivery_time).minute < 59)):
        delivery_time = input('Format invalid. Enter time (HH:MM) to check delivery statuses: ')

    time_object = convert_time(delivery_time)

    total_distance = 0

    # Load packages onto trucks and send for delivery at appropriate times
    # O(N) - 3 Departure times
    for i in range(0, len(departure_times)):
        if convert_time(departure_times[i]) < time_object:
            # O(N^2)
            nth_delivery_truck = load_delivery(package_table, i, departure_times[i], truck_array)
            # O(N^2)
            nth_delivery = nth_delivery_truck.run_delivery(departure_times[i], delivery_time, package_table)
            total_distance += nth_delivery[0]

    print('Total Distance for All Trips: {}'.format(round(total_distance, 2)))

    print()
    print("STATUS OF PACKAGES AT {}:".format(display_time(time_object)))

    # Display status of packages if any packages are in that state
    #  O(1)
    if len(package_table.delayed_packages) > 0:
        status_list = package_table.delayed_packages
        print("___________________")
        print()
        #  O(N^2)
        print('Delayed on flight: {}'.format(package_table.delayed_packages))
        # print_status_packages(status_list, package_table)

    # O(1)
    if len(package_table.wrong_address) > 0:
        status_list = package_table.wrong_address
        print("___________________")
        print()
        print('Awaiting address correction: {}'.format(status_list))
        # print_status_packages(status_list, package_table)

    # O(1)
    if len(package_table.ready) > 0:
        status_list = package_table.ready
        print("___________________")
        print()
        print('Ready for Delivery: {}'.format(status_list))
        # O(N^2)
        # print_status_packages(status_list, package_table)

    # O(1)
    if len(package_table.delivered) > 0:
        status_list = package_table.delivered
        print("___________________")
        print()
        print('Delivered: {}'.format(status_list))
        # print_status_packages(status_list, package_table)


    # O(N) - 3 Trucks
    for i in range(0, len(package_table.trucks)):
        status_list = package_table.trucks[i]
        if len(status_list) > 0:
            print("___________________")
            print()
            print("Out for Delivery on Truck {}: {}".format(str(i + 1), str(status_list)))
            # O(N^2)
            # print_status_packages(status_list, package_table)
    print()


def status_lookup(departure_times, truck_array):
    # Have user input a validly formatted time to check package at
    check_time = input('Enter time (HH:MM): ')
    while (convert_time(check_time) is False) or not ((0 <= convert_time(check_time).hour < 24) and (0 <= convert_time(check_time).minute < 59)):
        check_time = input('Format invalid. Enter time (HH:MM) to check package status: ')

    time_object = convert_time(check_time)
    package_id = input('Please enter a package ID to look up: ')

    package_table = load_packages()

    # O(N) - 3 departure times
    for i in range(0, len(departure_times)):
        # Run delivery only if it has passed the truck departure time
        if convert_time(departure_times[i]) < time_object:
            # O(N^2)
            nth_delivery = load_delivery(package_table, i, departure_times[i], truck_array)
            # O(N^2)
            nth_delivery.run_delivery(departure_times[i], check_time, package_table)

    # Search for desired package after running delivery
    # O(N)
    package_result = package_table.search(int(package_id))

    # Display formatted package information
    # O(1)
    if package_result is None:
        print()
        print("No package found")
    else:
        print("STATUS OF PACKAGE AT {}:".format(display_time(time_object)))
        package_result.print()


def main():
    # Display user interface in console to accept user requests for different functions
    print('Welcome to the WGUPS Routing Program')
    user_request = input('Type "1" to look up a package, "2" to run delivery, or "exit" to quit program ')

    # Have user a validly formatted time to check delivery status at
    departure_times = ['8:00 AM', '9:05 AM', '10:25 AM']

    # Create list of available trucks for delivery
    truck_num = 3
    truck_array = []
    for i in range(1, truck_num+1):
        truck = Truck(i)
        truck_array.append(truck)

    while user_request != 'exit':
        if user_request == '1':
            status_lookup(departure_times, truck_array)
            user_request = input('Type "1" to look up a package, "2" to run delivery, or "exit" to quit program ')

        elif user_request == '2':
            delivery(departure_times, truck_array)
            user_request = input('Type "1" to look up a package, "2" to run delivery, or "exit" to quit program ')

        elif user_request == 'exit':
            exit()

        else:
            print('Invalid entry!')
            user_request = input('Type "1" to look up a package, "2" to run delivery, or "exit" to quit program ')


if __name__ == "__main__":
    main()
