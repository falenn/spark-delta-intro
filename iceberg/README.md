# Demo!
https://www.dremio.com/blog/a-notebook-for-getting-started-with-project-nessie-apache-iceberg-and-apache-spark/

Tutorial on Spark / Iceberg / Nessie / Dremio / MinIO
https://www.youtube.com/watch?v=X3wfVaSQS_c&t=134s


## Spark Configuration
org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.0.0
org.projectnessie:nessie-spark-extensions-3.3_2.12:0.45.0

## Arrow-based columnar transfer
conf.set("spark.sql.execution.pyarrow.enabled","true")

## Config to write to object store
conf.set("spark.sql.catalog.arctic.io-impl","org.apache.iceberg.aws.s3.S3FileIO")

## Create a new catalog called 'artic' as an iceberg catalog
conf.set("spark.sql.catalog.artic","org.apache.iceberg.spark.SparkCatalog")

## Tell catalog that it's a Nessie Catalog
conf.set("spark.sql.catalog.artic.catalog-impl","org.apache.iceberg.nessie.NessieCatalog")

## Set the location for the catalog to the object store
conf.set("spark.sql.catalog.artic.warehouse","s3://bucket/")

## Set the location of the Nessie / Artic Server
conf.set("spark.sql.catalog.artic.uri","https://localhost:19120/api/vi")

## Authentication Mechanism
conf.set("spark.sql.catalog.artic.authentication.type","BEARER")
conf.set("spark.sql.catalog.artic.authentication.token","token")

## Spark SQL extensions - execute Nessie commands via SQL
org.apache.iceberg.spark.IcebergSparkSessionExtensions

# Setting up Nessie
Nessie can use DynamoDB for storage.  Hmmmm
## Docker
docker pull ghcr.io/projectnessie/nessie

### Super-basic startup.  Need to mount in some storage I think
docker run -p 19120:19120 ghcr.io/projectnessie/nessie

## install the python cli
pip install pynessie


## Notes on Nessie
Nessie functions like a git repo, storing table metadata via change transactions.

When configuring Nessie, there are variables to set that are a bit confusing.
### Variables

#### NESSIE_WAREHOUSE_PATH
```
NESSIE_WAREHOUSE_PATH="file:///home/cloud_user/spark_warehouse/iceberg"
```
Iceberg documentation says this:
"Like most other catalogs the warehouse property is a file path to where this catalog should store tables."

This is not helpful as we are wanting the catalog stored in Mongodb.  It appears as though Nessie info stored in Mongo is about the 
transactional nature of catalog metadata only.

Since the interaction with Nessie is like Git, then maybe the warehouse path is temp space?

## Notes on MinIo
MinIO is S3-compatable storage  :)

### Cmdline
Install cmdline client
```
sudo curl -o /usr/local/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc

sudo chmod +x /usr/local/bin/mc

mc --version

mc alias set myminio http://localhost:9000 minioadmin minioadmin
```

Create bucket
```
mc mb myminio/<bucketname>
```

Copy data 
```
 mc cp states_2022*.avro myminio/flightdata/states
```

List Bucket contents
```
mc ls myminio/
```

