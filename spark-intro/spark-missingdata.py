#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark.sql.functions import mean

# Create the spark session
spark = SparkSession.builder.appName('appl').getOrCreate()

# Read in CSV data
df = spark.read.csv('../data/ContainsNull.csv',inferSchema=True,header=True)

# Show the schema
df.printSchema()
# Show the data
df.show()

# we can drop all missing data
df.na.drop().show()

# we can drop some of the rows giving a threshhold of null values
df.na.drop(thresh=2).show()

# drop row if any columns are null
df.na.drop(how='any').show()

# drop row if all columns are null
df.na.drop(how='all').show()

# drop only if value in sales is null
df.na.drop(subset=['Sales']).show()

# Now, we want to fill in values instead of drop:
df.na.fill('Fill Value').show() # fills in String types with a string
df.na.fill(0).show() # fills in number in Numeric type

#However, better to specify the column
df.na.fill('NONAME',subset=['Name']).show()

# And for the sales, lets fill in the missing numbers with the mean 
# from all the other numbers (this way the mean is not tampered with by# filling in wtih 0s)
mean = df.select(mean('Sales')).collect()
# mean is now a list of rows
print(f"mean: {mean}")

# get first row, get first column in that row using indexing
mean = mean[0][0]

# Fill in missing Sales values with the mean
df.na.fill(mean,['Sales']).show()
