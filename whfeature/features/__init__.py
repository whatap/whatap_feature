from . import kafka, vcenter, aerospike, apachepulsar, nginx, apache, milvus

allFeatures = [kafka.getMainArgs(),vcenter.getMainArgs(), 
               aerospike.getMainArgs(), apachepulsar.getMainArgs(),
               nginx.getMainArgs(), apache.getMainArgs(), milvus.getMainArgs()]
features = {}
kafka.update(features)
vcenter.update(features)
aerospike.update(features)
apachepulsar.update(features)
nginx.update(features)
apache.update(features)
milvus.update(features)

def listAll():
    return allFeatures

def getByTextKey(tk):
    return features.get(tk)

