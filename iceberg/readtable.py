#!/usr/bin/env python

import os
import findspark
from pyspark.sql import *
from pyspark import SparkConf
from pyspark.sql.types import DoubleType, FloatType, LongType, StructType, StructField, StringType

findspark.init()

conf = SparkConf()

spark = SparkSession.builder.config(conf=conf).getOrCreate()
print("Read Table")

#schema = StructType([
#    StructField("vendor_id", LongType(), True),
#    StructField("trip_id", LongType(), True),
#    StructField("trip_distance", FloatType(), True),
#    StructField("fare_amount", DoubleType(), True),
#    StructField("store_and_fwd_flag", StringType(), True)
#])

#df = spark.createDataFrame([], schema)
#df.writeTo("nyc_taxis").create()

tables = spark.sql("SHOW TABLES IN nessie.default").collect()

for table in tables:
        print(table.tableName)




