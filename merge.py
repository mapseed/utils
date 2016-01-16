#!/usr/bin/env python
from __future__ import print_function
# import code
# from time import sleep
import csv
import argparse

__author__ = "Luke Swart"

"""
This is a many-to-one merge script that takes a 'merge-many' csv,
and for every row, joins it with a 'merge-one' csv file,
and outputs the result to an 'output' file
"""

# The column names of the two spreadsheets that we are joining:
MERGE_MANY_REFERENCE_COLUMN = 'ID'
MERGE_ONE_REFERENCE_COLUMN = 'ID'

# An array of column names for the columns that will be merged.
# TODO: If the column names between the merge and destination csv's are not
# identical, use an array of tuples containing the matching merge and
# destination columns
OVERRIDING_COLUMNS = ['PROJECT_DATE', 'END_DATE', 'LOCATION_LATITUDE',
                      'LOCATION_LONGITUDE', 'LOCATION_LINK']


def run():
    # Define our CLI arguments
    # example usage: `python etl.py -m rain raingardensTest.csv test.csv`
    parser = argparse.ArgumentParser(
        description="Many-to-one merge of one csv into another")

    parser.add_argument('merge_many', type=argparse.FileType('r'),
                        help='merge csv file')

    parser.add_argument('merge_one', type=argparse.FileType('r'),
                        help='merge_one csv file')

    parser.add_argument('destination', type=argparse.FileType('w'),
                        help='output csv file')

    parser.add_argument('-m', '--method', dest="method",
                        default="urban_waters",
                        help="Defines which method will process the file")

    args = parser.parse_args()

    print("starting merge script")
    print(args)
    if args.method == "urban_waters":
        print("merge_many:", args.merge_many)
        print("merge_one:", args.merge_one)
        print("output:", args.destination)
        with args.merge_many as merge_many_file,\
             args.merge_one as merge_one_file,\
             args.destination as destination_file:
            merge(merge_many_file, merge_one_file, destination_file)
        print("merged csv complete!")


def merge(merge_many_file, merge_one_file, destination_file):
    merge_many_reader = csv.DictReader(merge_many_file)
    merge_one_reader = csv.DictReader(merge_one_file)
    # Uncomment this for testing in interactive mode
    # code.interact(local=locals())
    fieldnames = merge_one_reader.fieldnames
    print("fieldnames:", fieldnames)
    destinationWriter = csv.DictWriter(destination_file, fieldnames=fieldnames)
    destinationWriter.writeheader()
    # merge_one_ids = []
    for row in merge_one_reader:
        reference_value = row[MERGE_ONE_REFERENCE_COLUMN]
        print("reference value:", reference_value)
        # merge_one_ids.append(reference_value)
        matching_many_rows = [check_row for check_row in merge_many_reader
                              if check_row[MERGE_MANY_REFERENCE_COLUMN] ==
                              reference_value]
        print("matching_many_rows:", matching_many_rows)
        for matching_many_row in matching_many_rows:
            for column in OVERRIDING_COLUMNS:
                new_row = row
                # If the row had nested (mutable) data types,
                # we'd need to clone it (can also use copy.deepcopy()):
                # new_row = dict((k,v) for k,v in row.items())
                new_row[column] = matching_many_row[column]
            print("writing new_row:", new_row)
            destinationWriter.writerow(new_row)
        if len(matching_many_rows) == 0:
            print("No matching rows for id:", reference_value)
            destinationWriter.writerow(row)
        merge_many_file.seek(0)
        merge_many_reader = csv.DictReader(merge_many_file)
    # Check for any unmatched rows in our merge_many_reader.
    # If so, migrate them over to our merge_one_reader.
    for row in merge_many_reader:
        reference_value = row[MERGE_MANY_REFERENCE_COLUMN]
        matching_one_rows = [row for row in merge_one_reader
                             if row[MERGE_ONE_REFERENCE_COLUMN] ==
                             reference_value]
        if len(matching_one_rows) > 0:
            print("No matching one rows associated with the many row id:",
                  reference_value)
            print("unmatched row:",
                  row)


def main():
    run()

if __name__ == '__main__':
    main()
