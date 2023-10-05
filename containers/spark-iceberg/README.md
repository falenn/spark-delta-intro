# Building an image for PySpark / Iceberg

## Default Tooling - docker-image-tool.sh
https://github.com/apache/spark/blob/master/bin/docker-image-tool.sh

This tooling, by convention adds expected script helpers that the driver can call to prepare the image to run your code / job.

More on this: 
https://atirek-ak.medium.com/building-an-apache-spark-image-from-spark-binaries-fe1adeb9a964

Download the correct spark version:
```
wget https://dlcdn.apache.org/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xvf spark-3.5.0-bin-hadoop3.tgz
```
CD to the docker-image-tool.sh
```
cd spark-3.5.0-bin-hadoop3
```

Run the build tool to generate a local docker image binary (for either python or Java)
```
./bin/docker-image-tool.sh -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```

Now, there's a small base image to use in YOUR Dockerfile.  This is what you set the FROM to.
