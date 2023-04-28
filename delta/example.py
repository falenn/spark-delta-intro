#!/usr/bin/env python

import pyspark
from delta.tables import *
from pyspark.sql.functions import *
from delta import *

# init a spark app
builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Another way to load a table
deltaTable = DeltaTable.forPath(spark, "/tmp/delta-table")

# update every even value by adding 100 to it
deltaTable.update(
  condition = expr("id % 2 == 0"),
  set = { "id": expr("id + 100") })



deltaTable.toDF().show()

