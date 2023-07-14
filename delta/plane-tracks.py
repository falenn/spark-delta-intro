#!/usr/bin/env python

import pyspark
from delta.tables import *
#from pyspark.sql.functions import *
from pyspark.sql.functions import sum,avg,max,min,mean,count
from delta import *
import argparse


# read in callsign param
parser = argparse.ArgumentParser()
parser.add_argument("--callsign",help="callsign you want more info on")
args = parser.parse_args()
if args.callsign:
    callsign = args.callsign
    # remove any whitespace
    callsign = callsign.strip()

if callsign is None:
    print(f"Error, --callsign must be set")
    exit(1)

# init a spark app
builder = pyspark.sql.SparkSession.builder.appName("Plane-detail: {callsign}") \
#  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
# Set logging level
spark.sparkContext.setLogLevel("WARN")

# Another way to load a table
delta_table = DeltaTable.forPath(spark, "/tmp/delta/states")
df_latest = delta_table.toDF()

print(f"{df_latest.schema}")

# get total record count
print(f"Total records: {df_latest.count()}")

# show history of mods to the table
delta_table.history().select("version", "timestamp", "operation", "operationParameters").show(10, False)

# select now using sparkSQL.  
df_latest.createOrReplaceTempView("states_latest")

print(f"Searching for records for callsign: {callsign}")

distinct_callsign_query = "SELECT distinct(callsign) from states_latest"
result = spark.sql(distinct_callsign_query)
print(f"Distinct Callsigns: {result.count()}")
result.show(10)

# Adding a space in the query for callsign - looks like need to clean the data
query = "SELECT * FROM states_latest WHERE callsign like \"{} \" ORDER BY time ASC".format(callsign)
print(f"SQL Statement: {query}")

result = spark.sql(query)

# Show count
print(f"Number of records found for {callsign}: {result.count()}")

# show some records
result.show(truncate = False)

