#!/usr/bin/env python

import os
import findspark
from pyspark.sql import *
from pyspark import SparkConf

findspark.init()

conf = SparkConf()

spark = SparkSession.builder.config(conf=conf).getOrCreate()
print("Spark Running")
