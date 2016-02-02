#!/usr/bin/env python

from __future__ import print_function
# import code
from time import sleep
import csv
import argparse
# from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3

__author__ = "Luke Swart"


def etl():
    # Define our CLI arguments
    # example usage: `python etl.py -m rain raingardensTest.csv test.csv`
    parser = argparse.ArgumentParser(description="Manage various etl tasks")

    parser.add_argument('input', type=argparse.FileType('r'),
                        help='input csv file')

    parser.add_argument('output', type=argparse.FileType('w'),
                        help='output csv file')

    parser.add_argument('-m', '--method', dest="method",
                        default="rain",
                        help="Defines which method will process the file")

    args = parser.parse_args()

    print(args)
    if args.method == "rain":
        print("input:", args.input)
        print("output:", args.output)
        with args.input as readFile, args.output as writeFile:
            process_rain_gardens(readFile, writeFile)
        print("transformed csv from", args.output, "into", args.input)
    elif args.method == "geocode":
        from geocode import geocode
        with args.input as readFile, args.output as writeFile:
            geocode(readFile, writeFile)
        print("transformed csv from", args.output, "into", args.input)


def process_rain_gardens(readFile, writeFile):
    print("process_rain_gardens!")
    # csv_from_master_list(master_list)
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
        lat = row['Lat']
        lon = row['Long']
        if not [True for v in row.values() if v.strip()]:
            print("Empty row:", row, ", skipping and continuing...")
            continue

        if lat == '' or lon == '':
            # print("replace lat/lon for row :", row)

            street_address = row['Street Address']

            zipcode = row['Zip Code']

            city = row['City']

            full_address = [street_address, city, 'WA', zipcode]
            address_list = [x for x in full_address if (x and x != 'NULL')]

            # garden_address = ', '.join(address_list)
            # location = geolocator.geocode(garden_address)
            location = None

            # snip off least-significant location until we get a location
            while not location:
                garden_address = ', '.join(address_list)
                print("address_list:", address_list)
                location = geolocator.geocode(garden_address)
                sleep(5)
                address_list = address_list[1:]
                if len(address_list) == 0:
                    raise Exception("\n\n\nNO LOCATION FOUND FOR ADDRESS:",
                                    full_address, "at row:", row, "\n\n\n")

            print("full_address:", full_address)
            row['Lat'] = str(location.latitude)
            row['Long'] = str(location.longitude)

        writer.writerow(row)


def main():
    etl()

if __name__ == '__main__':
    main()
