from . import kafka

allFeatures = [kafka.getMainArgs(),]
features = {}
kafka.update(features)

def listAll():
    return allFeatures

def getByTextKey(tk):
    return features.get(tk)
