##############################################################################
# precision_test.py
# https://github.com/DigiLog-N/DigiLog-N
# Copyright 2020 Canvass Labs, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

# Read PHM08 data from Apache Plasma in-memory data store
#
# This script shows sample commands for reading data from Plasma.
#
# Works with PHM08 data that has been written to Plasma by the CT2Arrow.
#
# The schema for these record batches is as follows:
#
# ct_timestamp: double
# unit: int32
# time_cycles: int32
# op1: float
# op2: float
# op3: float
# sensor01: float
# sensor02: float
# sensor03: float
# sensor04: float
# sensor05: float
# sensor06: float
# sensor07: float
# sensor08: float
# sensor09: float
# sensor10: float
# sensor11: float
# sensor12: float
# sensor13: float
# sensor14: float
# sensor15: float
# sensor16: float
# sensor17: float
# sensor18: float
# sensor19: float
# sensor20: float
# sensor21: float
#
# John P. Wilson, Erigo Technologies
# Charles Cowart, Canvass Labs, Inc.
#
# Will Common Data Layer (CDL) be comprised of one large Plasma shared memory
# file, or multiple files? If we assume a single file with a path_name fixed
# at configuration, then when we pull objects from Plasma, we have to know
# what data source it is, whether it's new or not, etc. We also need to be
# able to filter the list for new items, hopefully without maintaining our
# own list.
#
# If the CDL is comprised of an arbitrary number of Plasma files, then each
# Plasma file can be dedicated to a specific data source, in this case, engine
# data. However, without a pathway to the file or a directory to scan for
# files, we lose the ability to discover new data sources. Perhaps the fixed
# path to discover new files is the best approach.
#
# If we assume all Objects are for the same data source, and the data source
# will not be modified (for now), then we can assume that the schema is
# homogenous and will remain fixed.
#
# From here, we can map Plasma data types to Cassandra data types and auto-
# generate a new schema, create it in Cassandra, and insert the data in bulk
# with prepared statements.
#
# Using DataFrames as an intermediary was looked into, but there's no feature
# to auto-generate a Cassandra schema, so there is nothing gained.
#
# This code functions as a loader for both Cassandra and Mongo, and PySpark.
# An instance of this code will need to be present in the PySpark code as
# well, as we are not developing an interface to push data to PySpark.


import pyarrow as pa
import pyarrow.plasma as plasma
import numpy as np
import sys
import pandas as pd 
import csv

class PlasmaReader:
    def __init__(self, file_path):
        self.client = plasma.connect(file_path)
        self.refresh_keys()
        self.d = {}

    def refresh_keys(self):
        # generates a list of keys to objects currently in the Plasma store.
        # this method is called at construction, and the list of keys can
        # be refreshed any time this method is called by the user.
        l = list(self.client.list().keys())

        # currently the only way I know to remove the ObjectID description
        # from the id itself.
        l = [str(x).replace('ObjectID(', '').rstrip(')') for x in l]

        # the ids in l are encoded in hex, and thus not human-readable. This
        # will allow us to get a human-browsable list.
        l = [bytearray.fromhex(str(x)).decode() for x in l]

        self.keys = l

    def do_something(self, key):
        # Fetch one object from Plasma
        id = plasma.ObjectID(key.encode())

        # Read data from the Plasma object
        # Each Plasma object written out from CT2Arrow only contains 1 record batch
        # Examine the data from this record batch
        # (see https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatch.html#pyarrow.RecordBatch)
        [data] = self.client.get_buffers([id])
        reader = pa.RecordBatchStreamReader(pa.BufferReader(data))

        batch = reader.read_next_batch()
        #print(key)
        #print('number of columns = %d' %(batch.num_columns))
        #print('number of rows = %d' % (batch.num_rows))
        #print('schema:')

        # generate Cassandra schema from the metadata output from this method.
        #        import pdb; pdb.set_trace()
        #print(batch.schema)

        header = batch.schema.names

        for i in range(0, batch.num_columns):
            #d[header[i]] = pd.Series(batch.column(i).to_pylist())
            column = header[i]
            if not column in self.d:
                self.d[header[i]] = []

            self.d[header[i]] += batch.column(i).to_pylist()

        # note that 60 rows of data for Engine Unit 38 is in PHM08********_b00102,
        # while the final 29 is in PHM08********_b00103. Each Object contains
        # data for only one Engine Unit (Confirmed). Hence, final confirmation
        # requires iterating through all Objects.


if __name__ == '__main__':
    pr = PlasmaReader('/tmp/plasma')
    for key in pr.keys:
        pr.do_something(key)

    # Convert the dictionary of lists into a Pandas DataFrame
    # Start by converting each list into a Series object
    for column in pr.d:
        pr.d[column] = pd.Series(pr.d[column])

    # Turn the dictionary of Series objects into a DataFrame,
    # where the dictionary keys become the column names.
    frame = pd.DataFrame(pr.d)

    # remove the added ct_timestamp column in order to make the comparison
    # easier.
    frame = frame.drop(columns=['ct_timestamp'])

    # sort the values as they are in the original sample, ordered by
    # engine unit and cycle number (time).
    frame = frame.sort_values(by=['unit', 'time'])

    # now that the frame has been reordered, reset the index numbers
    # for the rows to match those of the original sample.
    frame = frame.reset_index(drop=True)

    # let's open the original sample from a CSV file into a Pandas
    # DataFrame.
    original_frame = pd.read_csv('raw_first_five_engines.csv')

    # The objective is to compare the original text data loaded directly
    # into a Pandas dataframe, against the data output after it's migrated
    # from original text to Cloud Turbine to CT2Arrow, to Plasma.
    #
    # Verify that the number of columns is retained, the number of rows
    # are retained, and that the values are equal.
    original_frame['sensor17'] = original_frame['sensor17'].astype(float)
    original_frame['sensor18'] = original_frame['sensor18'].astype(float)

    # Uncommenting this will allow you to see that the frames are not
    # equal - there has been some change in the precision of the floating
    # point values as they traveled through the pipeline!
    # print(frame.eq(original_frame))

    # sanity check to verify that the row counts are equal:
    a = len(frame)
    b = len(original_frame)
    if a != b:
        print("row counts are not equal: %d vs %d" % (a, b))
        exit(1)

    # sanity check to verify that the column counts are equal:
    a = len(frame.columns)
    b = len(original_frame.columns)
    if a != b:
        print("column counts are not equal: %d vs %d" % (a, b))
        exit(1)

    # assuming that the dimensions of both dataframes are equal, let's
    # iterate through each cell and quantify the change in value:
    with open('deltas.csv', 'w', newline='') as csvfile:
        delta_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in range(0, len(frame)):
            l = []
            for column in range(0, len(frame.columns)):
                a = frame.loc[row][column]
                b = original_frame.loc[row][column]
                delta = a - b
                sum_of_deltas += abs(delta)
                cell_count += 1
                l.append(delta)
            delta_writer.writerow(l)

    # import the CSV file into a spreadsheet to calculate mean, median, and std dev
    # of the deltas.
