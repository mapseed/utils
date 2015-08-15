from __future__ import print_function
# import code
import csv
import argparse
from geopy.geocoders import Nominatim

__author__ = "Luke Swart"


def etl():
    # Define our CLI arguments
    parser = argparse.ArgumentParser(description="Manage various etl tasks")

    parser.add_argument('input', type=argparse.FileType('r'),
                        help='input csv file')

    parser.add_argument('output', type=argparse.FileType('w'),
                        help='output csv file')

    parser.add_argument('-m', '--method', action="store_true", dest="rain",
                        default=True,
                        help="Rain garden tranform type requested")
    args = parser.parse_args()

    print(args)
    if args.rain:
        # print("input:", args.input)
        # print("output:", args.output)
        with args.input as readFile, args.output as writeFile:
            process_rain_gardens(readFile, writeFile)
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
    geolocator = Nominatim()
    for row in reader:
        # if lat/lon not defined, then fill it in with the geocoding
        # Uncomment this for testing in interactive mode
        # code.interact(local=locals())
        lat = row['Lat']
        lon = row['Long']
        if lat == '' or lon == '':
            # print("replace lat/lon for row :", row)

            street_address = row['Street Address ']
            if street_address == 'NULL':
                street_address = ''

            zipcode = row['Zip Code ']
            if zipcode == 'NULL':
                zipcode = ''

            city = row['City']
            if city == 'NULL':
                city = ''

            full_address = [street_address, city, 'WA', zipcode]
            address_list = [x for x in full_address if x]

            # garden_address = ', '.join(address_list)
            # location = geolocator.geocode(garden_address)
            location = None

            # snip off least-significant location until we get a location
            while not location:
                garden_address = ', '.join(address_list)
                try:
                    location = geolocator.geocode(garden_address)
                except GeocoderTimedOut as e:
                    print("\n\n\nGEOCODER TIMED OUT FOR ADDRESS:",
                          full_address)
                    print("exception:", e, "\n\n\n")
                    # If there is a timeout, replicate the row.
                    location = {'latitude': '', 'longitude': ''}
                    break
                address_list = address_list[1:]
                if len(address_list) == 0:
                    raise Exception("\n\n\nNO LOCATION FOUND FOR ADDRESS:",
                                    full_address, "\n\n\n")

            print("adding address_list location:", address_list)
            print("for the full_address:", full_address)
            row['Lat'] = str(location.latitude)
            row['Long'] = str(location.longitude)

        writer.writerow(row)


def main():
    etl()

if __name__ == '__main__':
    main()
