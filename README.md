
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
https://realpython.com/intro-to-pyenv/#installing-pyenv

## Install PyEnv
### Setup to install alternate Python versions
```
sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite \
  sqlite-devel openssl-devel xz xz-devel libffi-devel
```

### Using the PyEnv installer
```
curl https://pyenv.run | bash
```
### Add the following to ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
 eval "$(pyenv init -)"
fi

### Using PyEnv to install Python
See available versions
```
pyenv install --list | grep " 3\.[678]"
```
Select and install:
```
pyenv install -v 3.7.2
```

## Using Pyenv
### See available versions
```
pyenv versions
```

### Create a virtual env with a given version

pyenv virtualenv <python_version> <environment_name>
```
pyenv virtualenv 3.9.17 iceberg_3-5
```

Switch to that virtualenv
```
pyenv local iceberg_3-5
```
This uses the .python-version file in the local dir
eval "$(pyenv virtualenv-init -)"   <-- this should be in your .bash_profile

If the python version is not changing, you probably have a global virtualenv set.  Deactivate it:
```
pyenv versions
```
notice the one that is marked with an astrick.  Deactivate it.
```
pyenv deactivate (currently active env)
```




# Install Maven
```
mkdir -p ~/apps/maven
cd ~/aps/maven
wget -O maven.tar.gz https://dlcdn.apache.org/maven/maven-3/3.9.2/binaries/apache-maven-3.9.2-bin.tar.gz
tar -xvf maven.tar.gz
ln -s ~/apps/maven/apache-maven-3.9.2 current
```
# Install Helpers
```
sudo yum install tmux wget git
```
# Install yq - YAML Query
```
BINARY=yq_linux_amd64 
LATEST=$(wget -qO- https://api.github.com/repos/mikefarah/yq/releases/latest 2>/dev/null | grep browser_download_url | grep $BINARY\"\$|awk '{print $NF}' )
sudo wget -q $LATEST -O /usr/bin/yq && sudo chmod +x /usr/bin/yq
```
# Install Docker

## RockyOS
### Check version
```
cat /etc/os-release
```

### Install RockyOS 8
```
sudo dnf check-update
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```
or add repo manually:
```
[docker-ce]
name=Docker-CE
baseurl=https://download.docker.com/linux/centos/8/x86_64/stable/
gpgcheck=0
enabled=1
```
Install
```
sudo dnf install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl status docker
sudo systemctl enable docker
```

## Grant access to a user
```
sudo usermod -aG docker $(whoami)
```

## Fixing SELinux issues
You can leave SELinux running and add additional rulees to accomodate Docker
```
audit2allow -a /var/log/audit/audit.log
grep docker_t /var/log/audit/audit.log | audit2allow -M my-docker-rules
semodule -i my-docker-rules
```

# Kubernetes
## Nice k8s install writeup for RockyOS
https://r00t.dk/post/2022/02/13/basic-kubernetes-installation-rocky-linux-rancher/

## KIND 
### Install
```
https://kind.sigs.k8s.io/docs/user/quick-start/#installation
```
or;
```
# For AMD64 / x86_64
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
# For ARM64
[ $(uname -m) = aarch64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-arm64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```
### Create Cluster
Cluster config - creating volume mount for data so that it persists outside of Docker / KIND on the host

KIND uses https://github.com/rancher/local-path-provisioner for CSI storage.  We need to map the dir used out of Docker to the host for persistence.
```
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: app-1-cluster
nodes:
# one node hosting a control plane
- role: control-plane
  extraMounts:
  - hostPath: /var/data
    containerPath: /var/local-path-provisioner
  extraPortMappings:
  - containerPort: 9000
    hostPort: 9000
    # optional: set the bind address on the host
    # 0.0.0.0 is the current default
    listenAddress: "127.0.0.1"
    # optional: set the protocol to one of TCP, UDP, SCTP.
    # TCP is the default
    protocol: TCP
```

Create dir on disk for this
```
sudo mkdir -p /var/data
sudo chmod 1777 /var/data
```

Create the cluster:
```
kind create cluster --config ~/dev/kind/cluster.yml
```

## kubectl
```
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```

## run a quick, inteactive pod to ensure basic functionality
```
kubectl run -i --tty --rm debug --image=busybox --restart=Never -- sh
```

## Install Helm
```
sudo curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
sudo chmod 700 get_helm.sh
sudo ./get_helm.sh
```

## Hashicorp Vault
We want a central location for Certificate management.  Vault is a FIPS-certified cryptographic store with other features much like an HSM

### Installation
https://developer.hashicorp.com/vault/docs/platform/k8s/helm
We will use Helm to install Vault within K8s

Add the repo
```
helm repo add hashicorp https://helm.releases.hashicorp.com
```

Search the repo for latest releases
```
helm search repo hashicorp/vault
```
or all releases
```
helm search repo hashicorp/vault -l
```

Fetch the chart
```
helm fetch vault  hashicorp/vault --untar=true --untardir=/home/cloud_user/dev/charts
```

Install vault after values.yaml mods
```
cd /home/cloud_user/dev/charts/vault
helm install vault  hashicorp/vault -f values.yaml
```

### Creating a CA
```

```
### PKI Certificate management within K8s


## Nginx Ingress
We want an ingress controller so that we do not have to open NodePorts for every service, instead, using URL rewriting, we can place them behind
one URL.
There are other features following this action.
### Install
```
[cloud_user@2b23a275812c nginx]$ helm install nginx bitnami/nginx -f values.yaml
NAME: nginx
LAST DEPLOYED: Wed Oct 25 04:11:19 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: nginx
CHART VERSION: 15.3.1
APP VERSION: 1.25.2

** Please be patient while the chart is being deployed **
NGINX can be accessed through the following DNS name from within your cluster:

    nginx.default.svc.cluster.local (port 80)

To access NGINX from outside the cluster, follow the steps below:

1. Get the NGINX URL by running these commands:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc --namespace default -w nginx'

    export SERVICE_PORT=$(kubectl get --namespace default -o jsonpath="{.spec.ports[0].port}" services nginx)
    export SERVICE_IP=$(kubectl get svc --namespace default nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    echo "http://${SERVICE_IP}:${SERVICE_PORT}"
```

## Minio S3
We will install using Helm.  First pull down the chart to get the values.yml to configure for our dev env.
https://www.datree.io/helm-chart/minio-bitnami
```
helm repo add bitnami https://charts.bitnami.com/bitnami
mkdir -p ~/dev/charts
cd ~/dev/charts
helm fetch bitnami/minio --untar=true --untardir=.
```
Review the values.yml file so that only 1 node is needed:
```
mode: standalone
...
persistence:
  storageClass: "" (Uses the default)
  mountPath: /bitnami/minio/data
```

### Install minio
```
helm install my-minio bitnami/minio -f ~/dev/charts/minio/values.yaml

```
Use --version to specify a specific version, e.g., --version 11.2.16

### Interactive minio-client container
```
export ROOT_USER=$(kubectl get secret --namespace default my-minio -o jsonpath="{.data.root-user}" | base64 -d)
export ROOT_PASSWORD=$(kubectl get secret --namespace default my-minio -o jsonpath="{.data.root-password}" | base64 -d)

kubectl run --namespace default my-minio-client \
     --rm --tty -i --restart='Never' \
     --env MINIO_SERVER_ROOT_USER=$ROOT_USER \
     --env MINIO_SERVER_ROOT_PASSWORD=$ROOT_PASSWORD \
     --env MINIO_SERVER_HOST=my-minio \
     --image docker.io/bitnami/minio-client:2023.9.13-debian-11-r2 -- /bin/bash
```

Let's test minio and the data volume mount - data should be seen on /var/data.  Start the Minio client above.  At the prompt, run:
```
mc mb test   # make a bucket called test
mc cp licenses/<one of the license files> test  # copy a file to test
```
Now check on the host for PVC creation in /var/data

### Install Minio Client
Install the Minio Client on the host.  We can use the port openned to k8s (9000) to connect to Minio from the client making loading of data easier.
```
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/

mc --help
```

## Nessie Metadata Catalog 
https://artifacthub.io/packages/helm/nessie/nessie

### Install Mongodb
```
helm fetch bitnami/mongodb --untar=true --untardir=$HOME/dev/charts
```
alter values - add usernames,passwors,databases (nessie for all three) to create an account and database at creation time.
```
cd $HOME/dev/charts/mongodb
helm install mongodb bitnami/mongodb -f values.yaml
```

Result from startup
```
helm install mongodb bitnami/mongodb -f values.yaml
NAME: mongodb
LAST DEPLOYED: Wed Sep 20 16:10:00 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: mongodb
CHART VERSION: 13.18.4
APP VERSION: 6.0.10

** Please be patient while the chart is being deployed **

MongoDB&reg; can be accessed on the following DNS name(s) and ports from within your cluster:

    mongodb.default.svc.cluster.local

To get the root password run:

    export MONGODB_ROOT_PASSWORD=$(kubectl get secret --namespace default mongodb -o jsonpath="{.data.mongodb-root-password}" | base64 -d)                                                                                       

To get the password for "nessie" run:

    export MONGODB_PASSWORD=$(kubectl get secret --namespace default mongodb -o jsonpath="{.data.mongodb-passwords}" | base64 -d | awk -F',' '{print $1}')                                                                       

To connect to your database, create a MongoDB&reg; client container:

    kubectl run --namespace default mongodb-client --rm --tty -i --restart='Never' --env="MONGODB_ROOT_PASSWORD=$MONGODB_ROOT_PASSWORD" --image docker.io/bitnami/mongodb:6.0.10-debian-11-r0 --command -- bash                  

Then, run the following command:
    mongosh admin --host "mongodb" --authenticationDatabase admin -u $MONGODB_ROOT_USER -p $MONGODB_ROOT_PASSWORD                                                                                                                

To connect to your database from outside the cluster execute the following commands:

    kubectl port-forward --namespace default svc/mongodb 27017:27017 &
    mongosh --host 127.0.0.1 --authenticationDatabase admin -p $MONGODB_ROOT_PASSWORD
```


### Fetch Nessie
```
helm repo add nessie-helm https://charts.projectnessie.org
helm repo update
cd ~/dev/charts
helm fetch nessie-helm/nessie --untar=true --untardir=.
```

### Modify values.yaml

### Install
```
helm install --namespace nessie-ns nessie nessie-helm/nessie -f ~/dev/charts/nessie/values.yaml
```

## Spark-Operator
We use the spark-operator to spin up a driver and executors for our spark applications within K8S.
https://www.youtube.com/watch?v=HaSHhYPIAhU for more info.
I feel that this is OLD. :(  I really wanted declarative scheduling...

## Bitnami/Spark
https://github.com/bitnami/charts/tree/main/bitnami/spark
Alternative to above - this is popular

### Installing
```
helm repo add bitnami oci://registry-1.docker.io/bitnamicharts

cd ~/dev/charts
helm fetch bitnami/spark --untar=true -untardir=.

helm install spark bitnami/spark -f ~/dev/charts/spark/values.yaml
```
The outcome of the install:
```
helm install spark bitnami/spark -f values.yaml
NAME: spark
LAST DEPLOYED: Sat Oct 21 20:28:07 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: spark
CHART VERSION: 8.0.0
APP VERSION: 3.5.0

** Please be patient while the chart is being deployed **

1. Get the Spark master WebUI URL by running these commands:

  kubectl port-forward --namespace default svc/spark-master-svc 80:80
  echo "Visit http://127.0.0.1:80 to use your application"

2. Submit an application to the cluster:

  To submit an application to the cluster the spark-submit script must be used. That script can be
  obtained at https://github.com/apache/spark/tree/master/bin. Also you can use kubectl run.

  export EXAMPLE_JAR=$(kubectl exec -ti --namespace default spark-worker-0 -- find examples/jars/ -name 'spark-example*\.jar' | tr -d '\r')                                                                                      

  kubectl exec -ti --namespace default spark-worker-0 -- spark-submit --master spark://spark-master-svc:7077 \
    --class org.apache.spark.examples.SparkPi \
    $EXAMPLE_JAR 5

** IMPORTANT: When submit an application from outside the cluster service type should be set to the NodePort or LoadBalancer. **                                                                                                 

** IMPORTANT: When submit an application the --master parameter should be set to the service IP, if not, the application will not resolve the master. **
```
In running the first example, the jar is already on the spark worker.
Also, when port-forwarding, I did forward to 30081:80 not, 80:80. 

The example submits the job using a worker as the exec target to show the distinct DNS resolve to the master node:
```
kubectl exec -ti --namespace default spark-worker-0 -- (the command to run on the spark-worker-0 is to follow) spark-submit --master spark://spark-master-svc:7077 \
    --class org.apache.spark.examples.SparkPi \
    $EXAMPLE_JAR 5
```

To scale up the number of workers:
```
helm upgrade spark bitnami/spark --set worker.replicaCount=3
```


### Test Spark Job
We will run a test job on the k8s spark cluster using the following bash script
```
#!/usr/bin/env bash

# Running spark-submit to run a Spark job on k8s using bitnami/spark chart.

PY_FILE="./spark-empty-schema.py"
SPARK_IMAGE="falenn/iceberg-python:1.0.1"
spark-submit \
        --conf "spark.sql.session.timeZone=UTC" \
        --deploy-mode "cluster" \
        --name "k8s-helloworld" \
        --conf spark.executor.instances="2" \
        --conf spark.kubernetes.container.image="$SPARK_IMAGE" \
        --master k8s://https://localhost:39883 \
        $PY_FILE
```
The job spark-empty-schema.py is in spark-intro directory.  We will try to add the custom image we are building.



## Harbor 
@STILL WORKING ON THIS
### Install
```
cd ~/dev/charts
helm fetch bitnami/harbor --untar=true --untardir=.
helm install harbor bitnami/harbor -f values.yaml -n harbor
```

Output:
```
helm install harbor bitnami/harbor -f values.yaml -n harbor
NAME: harbor
LAST DEPLOYED: Tue Sep 26 14:16:15 2023
NAMESPACE: harbor
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: harbor
CHART VERSION: 18.0.1
APP VERSION: 2.9.0

** Please be patient while the chart is being deployed **

1. Get the Harbor URL:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc --namespace harbor -w harbor'
    export SERVICE_IP=$(kubectl get svc --namespace harbor harbor --template "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")                                                                               
    echo "Harbor URL: http://$SERVICE_IP/"

2. Login with the following credentials to see your Harbor application

  echo Username: "admin"
  echo Password: $(kubectl get secret --namespace harbor harbor-core-envvars -o jsonpath="{.data.HARBOR_ADMIN_PASSWORD}" | base64 -d)
```


TODO 
need to install Mongodb for Nessie
need to add svc config for NodePort to Minio.
need to add svc to nodePort 30900 and then to KIND k8s up
checkout https://faun.pub/what-is-minio-and-how-to-configure-it-in-kubernetes-18072ac80fb2
need to research storage / install choice for Minio.  Is it possible to install as statefulset / bare metal volumes?  Is on Ceph going to slow it down?  Other options just for Minio storage performance.

# Helpers
## ssh config
```
IdentityFile ~/.ssh/id_rsa
User cloud_user

Host k8s
    Hostname <hostname running k8s api server>
    LocalForward 39883 127.0.0.1:39883  # kubectl
```

## K8s lightweight metrics API
```
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install my-metrics-server metrics-server/metrics-server --version 3.11.0
```
