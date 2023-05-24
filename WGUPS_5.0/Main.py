# WGUPS Vehicle Routing Program
# Written by: Joseph Jonson
# Student ID: 001171598

import csv
import datetime
import Truck
from HashTable import HashMap
from Package import Package

# Parse package information
with open("WGUPS Package file.csv") as csv_file:
    package_data = csv.reader(csv_file)
    package_data = list(package_data)

# Parse distance information
with open("distances.csv") as csv_file1:
    distance_data = csv.reader(csv_file1)
    distance_data = list(distance_data)

# Parse address information
with open("addresses.csv") as csv_file2:
    address_data = csv.reader(csv_file2)
    address_data = list(address_data)


# Function to add file data with hash_table.
# Creates package object 'p' to hold attributes and insert them into myHash hash_table.
# O(N)
def load_package_data(filename, myHash):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            dead_line = package[5]
            mass = package[6]
            delivery_status = "At Hub"

            # Package object
            p = Package(id, address, city, state, zipcode, dead_line, mass, delivery_status)

            # Insert data into hash table
            myHash.insert(id, p)


# Function that takes two index values, and converts them into a float type distance.
# O(N)
def get_miles(x_value, y_value):
    distance = distance_data[x_value][y_value]
    if distance == '':
        distance = distance_data[y_value][x_value]

    return float(distance)


# Function that compares an input address with the csv file and returns the first element in the tuple.
# O(N)
def get_address(address):
    for row in address_data:
        if address in row[2]:
            return int(row[0])


# Create truck object truck1
truck1 = Truck.Truck(16, 18, None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",
                     datetime.timedelta(hours=8))

# Create truck object truck2
truck2 = Truck.Truck(16, 18, None, [2, 3, 4, 5, 6, 8, 10, 11, 12, 18, 25, 36, 38], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Create truck object truck3
truck3 = Truck.Truck(16, 18, None, [7, 9, 17, 21, 22, 23, 24, 26, 27, 28, 32, 33, 35, 39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))


# Instantiate hashMap
# O(1)
myHash = HashMap()
# Insert packages into hash table
load_package_data("WGUPS Package file.csv", myHash)


# Function for delivering packages.
# Nearest Neighbor algorithm : O(n^2)
# Places all packages on truck passed through, into an array then clears the truck.
# While loop runs until array of packages have been compared.
def ship(truck):
    to_be_delivered = []
    for packageID in truck.packages:
        package = myHash.search(packageID)
        to_be_delivered.append(package)
    truck.packages.clear()

    # Adds the nearest package into the truck.packages list one by one
    while len(to_be_delivered) > 0:
        next_address = 9001
        next_package = None
        for package in to_be_delivered:
            if get_miles(get_address(truck.address), get_address(package.address)) <= next_address:
                next_address = get_miles(get_address(truck.address), get_address(package.address))
                next_package = package
        # Adds next closest package to the truck package list
        truck.packages.append(next_package.id)
        # Removes the same package from the not_delivered list
        to_be_delivered.remove(next_package)
        # Takes the mileage driven to this package into the truck.mileage attribute
        truck.mileage += next_address
        # Updates truck's current address attribute to the package it drove to
        truck.address = next_package.address
        # Updates the time it took for the truck to drive to the nearest package
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Ship all trucks on delivery route
ship(truck1)
ship(truck2)
ship(truck3)
truck1.depart_time = datetime.timedelta(hours=8)
truck2.depart_time = datetime.timedelta(hours=9, minutes=5)
truck3.depart_time = datetime.timedelta(hours=10, minutes=20)


# O(1)
def total_distance():
    total = truck1.mileage + truck2.mileage + truck3.mileage
    return total


# Main class that reports distance and delivery status for packages using a command line interface
# O(N)
class Main:
    # CLI Interface
    print("***************************************************")
    print("WGUPS Vehicle Routing Program: C950")
    print("***************************************************")
    print("\n")
    print("***************************************************")
    print("Total miles for all trucks:", total_distance())
    print("***************************************************")
    text = input("Type 'run' to initiate package search: ")
    print("\n")
    if text == "run":
        try:
            # The user will be asked to enter a specific time of the day (military time)
            package_time = input("Format is HH:MM:SS, and military time. Check the status of package(s) at: ")
            (h, m, s) = package_time.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            # The user will be asked if they want to see the status of all packages or only one
            search = input("Type 'search_one' to look up package by ID. For all packages type 'search_all': ")
            print("\n")
            # If input is "search_one" the program will ask for the package ID
            if search == "search_one":
                try:
                    # The user will be asked to input a package ID. Invalid entry will cause the program to quit
                    id = input("input package ID: ")
                    print("\n")
                    package = myHash.search(int(id))
                    package.update_status(convert_timedelta)
                    print(str(package))
                except ValueError:
                    print("Invalid. Exiting.")
                    exit()
            # If input is "search_all" all package information will print at once
            elif search == "search_all":
                try:
                    for packageID in range(1, 41):
                        package = myHash.search(packageID)
                        package.update_status(convert_timedelta)
                        print(str(package))
                except ValueError:
                    print("Invalid. Exiting.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Invalid. Exiting.")
            exit()
