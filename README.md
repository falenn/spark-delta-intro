
Spark-avro jar:
https://mvnrepository.com/artifact/org.apache.spark/spark-avro_2.13/3.4.0

# this one works
https://repo1.maven.org/maven2/org/apache/spark/spark-avro_2.12/2.4.8/spark-avro_2.12-2.4.8.jar

To run with spark-submit:

./bin/spark-submit --packages org.apache.spark:spark-avro_2.13:3.4.0



#Source python venv
#. ~/dev/python/bin/activate


function pyspark_shell() {
  pyspark --packages io.delta:delta-core_2.12:2.1.0 \
  --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
  --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
  --packages "org.apache.spark:spark-avro_2.12:3.4.0"
}

function spark_submit() {
  spark-submit \
        --packages "io.delta:delta-core_2.12:2.1.0,org.apache.spark:spark-avro_2.13:3.4.0" \
        --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
        --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
        --conf "SPARK_EXTRA_CLASSPATH=/home/cloud_user/dev/lib/spark-avro_2.13_3.4.0.jar" \
        --deploy-mode client \
        $@
}

# Setup pyenv

## Install PyEnv
curl https://pyenv.run | bash

## Add the following to ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
 eval "$(pyenv init -)"
fi

Install Maven
```
mkdir -p ~/apps/maven
cd ~/aps/maven
wget -O maven.tar.gz https://dlcdn.apache.org/maven/maven-3/3.9.2/binaries/apache-maven-3.9.2-bin.tar.gz
tar -xvf maven.tar.gz
ln -s ~/apps/maven/apache-maven-3.9.2 current
```
