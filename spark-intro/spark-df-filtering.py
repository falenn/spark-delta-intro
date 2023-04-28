#!/usr/bin/env python

from pyspark.sql import SparkSession

# Create the spark session
spark = SparkSession.builder.appName('appl').getOrCreate()

# Read in CSV data
df = spark.read.csv('../data/appl.csv',inferSchema=True,header=True)

# Show the schema
df.printSchema()

#Using combined SQL and DF syntax, we find the rows where the Closing price is less than 500
df.filter("Close < 500").select(['Date','Open','Close']).show()

# This is now we want to do things without SQL, but instead python
df.filter(df['Close'] < 500).select(['Date','Volume']).show()

# Dataframe count
rows = df.count()
cols = len(df.columns)
print(f"DF Dimensions: {(rows,cols)}")

# Total Number of rows - using SparkSQL
df.createOrReplaceTempView("AAPL")
spark.sql("SELECT COUNT(*) from AAPL").show()


