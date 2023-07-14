#!/usr/bin/env pytho


import pyspark
from delta.tables import *
#from pyspark.sql.functions import *
from pyspark.sql.functions import sum,avg,max,min,mean,count
from delta import *


# init a spark app
builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
#  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
#  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
# Set logging level
spark.sparkContext.setLogLevel("WARN")

# Another way to load a table
delta_table = DeltaTable.forPath(spark, "/tmp/delta/states")

# update every even value by adding 100 to it
#deltaTable.update(
#  condition = expr("id % 2 == 0"),
#  set = { "id": expr("id + 100") })

df_latest = delta_table.toDF()

print(f"{df_latest.schema}")

# get a sample
#df_latest.select(["callsign","vertrate","onground","lastcontact","heading","velocity"]).show(5)


# get total record count
print(f"Total records: {df_latest.count()}")

# show history of mods to the table
delta_table.history().select("version", "timestamp", "operation", "operationParameters").show(10, False)

# select now using sparkSQL.  
df_latest.createOrReplaceTempView("states_latest")

spark.sql(
    """
    SELECT * from states_latest
    LIMIT(5)
    """
    ).show()

result = spark.sql(
    """
    SELECT callsign, vertrate from states_latest
    WHERE onground is false
    AND vertrate != "NaN"
    AND vertrate > 35 or vertrate < -35
    ORDER by vertrate desc
    """
    )

print(f"rapid fliers: {result.count()}")

# render flights in histogram by vertrate
df_latest.filter(df_latest['vertrate'] >= 35).filter(df_latest['vertrate'] != "NaN").groupBy("callsign").agg(max("vertrate"),avg("velocity")).show()


# another select
spark.sql(
   """
   SELECT distinct callsign from states_latest
   WHERE onground is false
   AND vertrate != "NaN"
   AND vertrate > 35 or vertrate < -35
   ORDER by callsign asc
   """
).show(10)

# distinct callsigns
spark.sql(
    """
    SELECT count(distinct callsign) from states_latest
    """
    ).show()
