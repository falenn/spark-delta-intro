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

# Find closing < 200 and openning > 200
# Notice the & for AND.  | would be used for OR.  Also, notice the parenthesis for grouping
df.filter( (df['Close'] < 200 ) & (df['Open'] > 200)).show()

# let's get a single record as DATA - Collect is used to get data back
# Returns lists of Row objects
result = df.filter(df['Low'] == 197.16).collect()
# Print the list
print(f"Results: {result}")
# Get a row
row = result[0]
# process as a Dictionary
print(f"Volume Traded: {row.asDict()['Volume']}")


