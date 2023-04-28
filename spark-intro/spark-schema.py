#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark.sql.types import (StructField,StringType,IntegerType,StructType)

spark = SparkSession.builder.appName('Basics').getOrCreate()

# We will define a schema instead of letting Spark discover it

# Define a schema for our data.  Data is data/people.json
data_schema = [StructField('age',IntegerType(), True),
               StructField('name',StringType(),True)]


final_struc = StructType(fields=data_schema)


# Now read in with the schema used
df = spark.read.json('../data/people.json',schema=final_struc)

#Show the contents
df.show()

# Show the schema - spark will have to infer this from the JSON
df.printSchema()

# get Columns
print(f"Columns: {df.columns}")

# return some info about the dataframe - showing a statistical summary of the numeric columns
df.describe().show()
