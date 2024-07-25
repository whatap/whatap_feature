from . import kafka, vcenter

allFeatures = [kafka.getMainArgs(),]
features = {}
kafka.update(features)
vcenter.update(features)

def listAll():
    return allFeatures

def getByTextKey(tk):
    return features.get(tk)
