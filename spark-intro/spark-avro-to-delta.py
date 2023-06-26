#!/usr/bin/env python

# tool for easy schema extraction
#import fastavro

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
avro_data = "/home/cloud_user/dev/spark-delta-intro/data/states_2022-06-27-00.avro"

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

df.write.format("delta").mode("overwrite").save("/tmp/delta-table/flightpath/states")

# Copy contents of Avro file into a Delta table
#deltaTable = DeltaTable.forPath(spark,"/tmp/delta-table/flightpath/states")

spark.close()
