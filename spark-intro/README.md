# Setup

##Python Libraries

```
pip install pyspark
pip install avro
```

List the versions of the libs installed
```
pip freeze
```

## Java JDK
As Spark is Java, Java / Scala support is needed
```
sudo yum install java-11-openjdk java-11-openjdk-devel

or

sudo dnf -y install wget curl
https://www.oracle.com/java/technologies/downloads/#java11
```

## PySpark and Avro
When using Avro with PySpark, notice that spark-avro is built for the version of pyspark.  

Discover your version of PySpark:
```
$ pip freeze
avro==1.11.1
py4j==0.10.9.5
pyspark==3.2.4
spark==0.2.1
typing_extensions==4.1.1
```
My pyspark version is 3.2.4.  This is the version family that I need for spark-avro.  I set that in 
my --packages for easier import managment.

org.apache.spark:spark-avro_2.12:3.2.4 - the 3.2.4 must match my pyspark version.  This, I set in my 
bash helper function for running spark_submit.

```
function spark_submit() {
  spark-submit --packages "io.delta:delta-core_2.12:2.1.0,org.apache.spark:spark-avro_2.12:3.2.4" \
          --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
          --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
          --deploy-mode client $@

  # --conf "SPARK_EXTRA_CLASSPATH=/home/cloud_user/dev/lib/spark-avro_2.13-3.4.0.jar" \
}
```
Notice, using --packages means that I don't have to set the SPARK_EXTRA_CLASSPATH.  I could do this instead 
if I use maven or gradle to download needed dependencies and build the classpath by hand.

# Downloading Sample Data
## Open-Sky
OpenSky contains a number of datasets concerning public aircraft.  The states data is available in AVRO format.
https://opensky-network.org/datasets/states/2022-06-27/00/
