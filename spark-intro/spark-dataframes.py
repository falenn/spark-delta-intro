#!/usr/bin/env python

from pyspark.sql import SparkSession

# Create sparkSession
spark = SparkSession.builder.appName('Basics').getOrCreate()

# Read in data 
df = spark.read.json('../data/people.json')

# get a column object
agecol = df['age']
print(f"Type: {type(agecol)}")


# get a dataframe with a single column - 
# best to select - more capable
df.select('age').show()

# Returns the first two rows in the dataframe
print(f"first 2 rows: {df.head(2)}")


# now a Row object
print(f"first row: {df.head(2)[0]}")
print(f"Type of row: {type(df.head(2)[0])}")

# now return columns - can select multiple columns
df.select(["age","name"]).show()

# add a column - must take in a type Column 
df.withColumn('newage',df['age']*2).show()


# rename a column
df.withColumnRenamed('newage','stuff')
df.printSchema()

# delete a colum
df.drop('stuff').show()

# Create SQL View for direct SQL
df.createOrReplaceTempView('people')

results = spark.sql("SELECT * from people")
results.show()

results = spark.sql("SELECT * from people WHERE age > 29")
results.show()


