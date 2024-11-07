#!/usr/bin/env bash

cd /home/whatap
wget https://archive.apache.org/dist/pulsar/pulsar-3.2.3/apache-pulsar-3.2.3-bin.tar.gz
tar xvfz apache-pulsar-3.2.3-bin.tar.gz
cd apache-pulsar-3.2.3
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export NODEID=3
vi conf/zookeeper.conf
httpServerEnabled=true
httpServerPort=8002
# Add the server configurations
server.1=192.168.1.31:2888:3888
server.2=192.168.1.29:2888:3888
server.3=192.168.1.79:2888:3888

echo "192.168.1.31 1.apachepulsar.local" |sudo tee -a /etc/hosts
echo "192.168.1.29 2.apachepulsar.local"  |sudo tee -a /etc/hosts
echo "192.168.1.79 3.apachepulsar.local"  |sudo tee -a /etc/hosts



mkdir -p data/zookeeper
echo "$NODEID" > data/zookeeper/myid  # Replace <id> with 1, 2, or 3 depending on the node


nohup bin/pulsar zookeeper > logs/zookeeper.stderrout.log 2>&1 &

vi conf/bookkeeper.conf
zkServers=192.168.1.31:2181,192.168.1.29:2181,192.168.1.79:2181


mkdir -p data/bookkeeper

bin/bookkeeper shell metaformat -nonInteractive
nohup bin/pulsar bookie > logs/bookie.stderrout.log 2>&1 &

vi conf/broker.conf
zookeeperServers=192.168.1.31:2181,192.168.1.29:2181,192.168.1.79:2181
configurationStoreServers=192.168.1.31:2181,192.168.1.29:2181,192.168.1.79:2181
clusterName=hsnam-0731

bin/pulsar initialize-cluster-metadata \
    --cluster hsnam-0731 \
    --zookeeper 192.168.1.31:2181,192.168.1.29:2181,192.168.1.79:2181 \
    --configuration-store 192.168.1.31:2181,192.168.1.29:2181,192.168.1.79:2181 \
    --web-service-url http://192.168.1.31:8080 \
    --web-service-url-tls https://192.168.1.31:8443 \
    --broker-service-url pulsar://192.168.1.31:6650 \
    --broker-service-url-tls pulsar+ssl://192.168.1.31:6651

nohup bin/pulsar broker  > logs/broker.stderrout.log 2>&1 &

