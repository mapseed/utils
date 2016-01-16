#!/usr/bin/env python
from __future__ import print_function
from time import sleep
import csv
import argparse
# from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

"""
This program takes an 'input' csv file and geocodes the lat/long columns
(if empty), and outputs the results to an 'output' file
"""

LAT_COLUMN = 'LOCATION_LATITUDE'
LON_COLUMN = 'LOCATION_LONGITUDE'

ADDRESS_COLUMN = 'Address / Location name'

__author__ = "Luke Swart"


def run():
    # Define our CLI arguments
    # example usage: `python etl.py -m rain raingardensTest.csv test.csv`
    parser = argparse.ArgumentParser(description="Manage various etl tasks")

    parser.add_argument('input', type=argparse.FileType('r'),
                        help='input csv file')

    parser.add_argument('output', type=argparse.FileType('w'),
                        help='output csv file')

    parser.add_argument('-m', '--method', dest="method",
                        default="geocode",
                        help="Defines which method will process the file")

    args = parser.parse_args()

    print(args)
    if args.method == "geocode":
        print("input:", args.input)
        print("output:", args.output)
        with args.input as readFile, args.output as writeFile:
            geocode(readFile, writeFile)
        print("geocoded csv from", args.input, "into", args.output)


def geocode(readFile, writeFile):
    reader = csv.DictReader(readFile)
    # Uncomment this for testing in interactive mode
    # code.interact(local=locals())
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
    writer.writeheader()
    # geolocator = Nominatim()
    geolocator = GoogleV3()
    for row in reader:
        # if lat/lon not defined, then fill it in with the geocoding
        # Uncomment this for testing in interactive mode
        # code.interact(local=locals())
        lat = row[LAT_COLUMN]
        lon = row[LON_COLUMN]
        # Skip empty rows:
        if not [True for v in row.values() if v.strip()]:
            print("Empty row:", row, ", skipping and continuing...")
            continue

        if lat == '' or lon == '':
            # print("replace lat/lon for row :", row)

            address = row[ADDRESS_COLUMN]

            # zipcode = row['Zip Code']

            # city = row['City']

            full_address = [address, 'WA']
            address_list = [x for x in full_address if (x and x != 'NULL')]

            final_address = ', '.join(address_list)
            location = geolocator.geocode(final_address)
            print("geocoded location:", location)
            sleep(5)

            # Use this if we want to generalize our addresses further:
            # location = None
            # snip off least-significant location until we get a location
            # while not location:
            #     garden_address = ', '.join(address_list)
            #     print("address_list:", address_list)
            #     location = geolocator.geocode(garden_address)
            #     sleep(5)
            #     address_list = address_list[1:]
            #     if len(address_list) == 0:
            #         raise Exception("\n\n\nNO LOCATION FOUND FOR ADDRESS:",
            #                         full_address, "at row:", row, "\n\n\n")

            # print("full_address:", full_address)
            row[LAT_COLUMN] = str(location.latitude)
            row[LON_COLUMN] = str(location.longitude)

        writer.writerow(row)


def main():
    run()

if __name__ == '__main__':
    main()
