#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct,avg,stddev
from pyspark.sql.functions import format_number

spark = SparkSession.builder.appName('groupby').getOrCreate()

# Read in the data
df = spark.read.csv('../data/sales_info.csv', inferSchema=True,header=True)

#Show some data
df.show()

#Show the schema
df.printSchema()

# groupBy company - there are now a bunch of functions
# The functions will operate on numerics
df.groupBy("Company").mean().show()
df.groupBy("Company").sum().show()
df.groupBy("Company").max().show()

# Using the aggregate function takes in a column and the function 
# to apply. It will not groupBy any column, just apply the function 
# across all rows
df.agg({'Sales':'sum'}).show()
df.agg({'Sales':'max'}).show()

# A combination of the two strategies:
group_data = df.groupBy("Company")
group_data.agg({'Sales':'max'}).show()
# This is a little more generalized apprach as the function is swappable - a.k.a, max

# Now, using SQL fuctions
df.select(countDistinct('Company')).show()

df.select(avg('Sales').alias('Average Sales')).show()

# StandardDev prints kinda nasty.  Let's add formatting
sales_std = df.select(stddev("Sales").alias("std"))
#Using the alias, specify the number of sig digits to show
sales_std.select(format_number('std',2)).alias('StdDev Sales').show()
# We call alias twice - first to make it more accessible, 2nd time for pretty

# Sorting!  Sort ascending (default)...
df.orderBy("Sales").show()

# Descending
df.orderBy(df['Sales'].desc()).show()

