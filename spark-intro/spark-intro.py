#!/usr/bin/env python

from pyspark.sql import SparkSession

# Create a sparkSession
spark = SparkSession.builder.appName('Basics').getOrCreate()

# Create a dataframe using json format
df = spark.read.json('../data/people.json')

#Show the contents
df.show()

# Show the schema - spark will have to infer this from the JSON
df.printSchema()

# get Columns
print(f"Columns: {df.columns}")

# return some info about the dataframe - showing a statistical summary of the numeric columns
df.describe().show()



