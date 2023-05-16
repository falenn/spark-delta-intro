#!/usr/bin/env python

# tool for easy schema extraction
#import fastavro

import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct,avg,stddev
from pyspark.sql.functions import format_number

spark = SparkSession.builder.appName('groupby').getOrCreate()

filename = "/home/cloud_user/dev/data/states_2022-06-27-00.avro"

# Get Avro Schema
reader = DataFileReader(open(filename,"rb"),avro.io.DatumReader())
schema = reader.meta

# Get schema using fastavro
# Open the Avro file in 'rb' mode - read | binary
#with open(filename, 'rb') as avro_file:
    # Get the schema from the file's header
#    schema = fastavro.schema.load_schema(avro_file)


print(schema)


# Load avro into spark dataframe
df = spark.read.format("avro").load(filename)

#Show some data
#df.show()

#Show the schema
df.printSchema()

df.show(11)

