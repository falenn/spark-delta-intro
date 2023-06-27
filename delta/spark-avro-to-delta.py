#!/usr/bin/env python

# tool for easy schema extraction
#import fastavro

import argparse
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct,avg,stddev
from pyspark.sql.functions import format_number

from delta.tables import *
from delta import *

builder = SparkSession.builder.appName('ingest-flightdata-avro2delta') \

#we need to config sparksession
my_packages = ["io.delta:delta-core_2.12:2.1.0"]
spark = configure_spark_with_delta_pip(builder,extra_packages=my_packages).getOrCreate()

# path to avro file
parser = argparse.ArgumentParser()
parser.add_argument("--inavro", help="Path and file to avro data")
parser.add_argument("--deltatable", help="Path to the delta table")
args = parser.parse_args()
if args.inavro:
        avro_data = args.inavro
if args.deltatable:
        delta_table = args.deltatable

print(f"Input avro: {avro_data}")
print(f"Output delta table: {delta_table}")

# Get Avro Schema
reader = DataFileReader(open(avro_data,"rb"),avro.io.DatumReader())
schema = reader.meta

# Get schema using fastavro
# Open the Avro file in 'rb' mode - read | binary
#with open(filename, 'rb') as avro_file:
    # Get the schema from the file's header
#    schema = fastavro.schema.load_schema(avro_file)


print(schema)


# Load avro into spark dataframe
df = spark.read.format("avro").load(avro_data)

#Show some data
#df.show()

#Show the schema
df.printSchema()

df.show(1)

df.write.format("delta").mode("append").save(delta_table)

# Copy contents of Avro file into a Delta table
#deltaTable = DeltaTable.forPath(spark,"/tmp/delta-table/flightpath/states")

spark.close()
