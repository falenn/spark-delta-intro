#!/usr/bin/env python

import pyspark
from delta.tables import *
#from pyspark.sql.functions import *
from pyspark.sql.functions import sum,avg,max,min,mean,count
from delta import *


# init a spark app
builder = pyspark.sql.SparkSession.builder.appName("Planes-on-Ground") \
#  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
# Set logging level
spark.sparkContext.setLogLevel("WARN")

# Another way to load a table
delta_table = DeltaTable.forPath(spark, "/tmp/delta-table/flightdata/states")

# update every even value by adding 100 to it
#deltaTable.update(
#  condition = expr("id % 2 == 0"),
#  set = { "id": expr("id + 100") })

df_latest = delta_table.toDF()

print(f"{df_latest.schema}")

# get total record count
print(f"Total records: {df_latest.count()}")

# show history of mods to the table
delta_table.history().select("version", "timestamp", "operation", "operationParameters").show(10, False)

# select now using sparkSQL.  
df_latest.createOrReplaceTempView("states_latest")

result = spark.sql(
    """
    SELECT callsign, icao24, lat, lon, onground from states_latest
    WHERE onground is true
    LIMIT(5)
    """
    )

# Show count
print(f"Number of planes on the ground: {result.count()}")

# show some records
result.show(10)


# render flights in histogram by vertrate
#df_latest.filter(df_latest['vertrate'] >= 35).filter(df_latest['vertrate'] != "NaN").groupBy("callsign").agg(max("vertrate"),avg("velocity")).show()
