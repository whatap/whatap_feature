from . import kafka, vcenter, aerospike, apachepulsar

allFeatures = [kafka.getMainArgs(),vcenter.getMainArgs(), aerospike.getMainArgs(), apachepulsar.getMainArgs()]
features = {}
kafka.update(features)
vcenter.update(features)
aerospike.update(features)
apachepulsar.update(features)

def listAll():
    return allFeatures

def getByTextKey(tk):
    return features.get(tk)
