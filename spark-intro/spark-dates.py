#!/usr/bin/env python

from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct,avg,stddev
from pyspark.sql.functions import format_number
from pyspark.sql.functions import (dayofmonth,hour,dayofyear,month,year,weekofyear,date_format)

spark = SparkSession.builder.appName('datetime').getOrCreate()

# Read in the data
df = spark.read.csv('../data/appl.csv', inferSchema=True,header=True)

#Show some data
df.show()

#Show the schema
df.printSchema()

# show first record
df.head(1)
# Here we see a Python datetime object: 2010, 1, 4, 0, 0
# year, month, day, hour, minute

df.select(dayofmonth(df['Date'])).show()

# Lets figure out the average closing price per year
# extract the year from the datetime, add it as a new column so that
# we can groupBy it.  Create a new dataframe for this
newdf = df.withColumn("Year",year(df['Date']))
# Notice the new column
newdf.show()
# Groupby and average
newdf.groupBy("Year").mean().show()
# notice the column names after mean runs.  Have to account for that
# in the next step...

result = newdf.groupBy("Year").mean().select(["Year","avg(Close)"])
result = result.withColumnRenamed("Avg(Close)","AvgClose")
result = result.select(['Year',format_number('AvgClose',2).alias("Average Closing Price")]).orderBy(result['Year']).show()


