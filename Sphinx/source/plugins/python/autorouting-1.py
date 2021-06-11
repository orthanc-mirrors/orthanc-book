import orthanc

def OnChange(changeType, level, resourceId):
    if changeType == orthanc.ChangeType.STABLE_STUDY:
        print('Stable study: %s' % resourceId)
        orthanc.RestApiPost('/modalities/sample/store', resourceId)

orthanc.RegisterOnChangeCallback(OnChange)
