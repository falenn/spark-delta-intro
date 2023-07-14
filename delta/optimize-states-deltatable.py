#!/usr/bin/env python

import pyspark
from delta.tables import *
#from pyspark.sql.functions import *
from delta import *


# init a spark app
builder = pyspark.sql.SparkSession.builder.appName("optimize") \
#  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
# Set logging level
spark.sparkContext.setLogLevel("WARN")



result = spark.sql(
    """
    OPTIMIZE '/tmp/delta/states'
    """
    )

