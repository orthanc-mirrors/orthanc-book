import orthanc
import json

def OnChange(changeType, level, resourceId):
    if changeType == orthanc.ChangeType.STABLE_STUDY:
        print('Stable study: %s' % resourceId)
        payload = { "Resources" : [resourceId] }
        orthanc.RestApiPostAfterPlugins('/dicom-web/servers/sample/stow', payload)

orthanc.RegisterOnChangeCallback(OnChange)
