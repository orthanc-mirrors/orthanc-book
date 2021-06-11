import orthanc

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.ORTHANC_STARTED:
        print('Started')

        with open('/tmp/sample.dcm', 'rb') as f:
            orthanc.RestApiPost('/instances', f.read())

    elif changeType == orthanc.ChangeType.ORTHANC_STOPPED:
        print('Stopped')

    elif changeType == orthanc.ChangeType.NEW_INSTANCE:
        print('A new instance was uploaded: %s' % resource)

orthanc.RegisterOnChangeCallback(OnChange)
