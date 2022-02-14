import orthanc
import os

def GetPath(uuid, contentType):
    # Returns the path where to store the given attachment
    return 'attachment-%d-%s' % (contentType, uuid)

def OnCreate(uuid, contentType, data):
    with open(GetPath(uuid, contentType), 'wb') as f:
        f.write(data)

def OnRead(uuid, contentType):
    with open(GetPath(uuid, contentType), 'rb') as f:
        return f.read()

def OnRemove(uuid, contentType):
    os.remove(GetPath(uuid, contentType))

orthanc.RegisterStorageArea(OnCreate, OnRead, OnRemove)
