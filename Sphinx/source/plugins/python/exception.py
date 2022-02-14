import orthanc

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.ORTHANC_STARTED:
        try:
            print(orthanc.RestApiGet('/nope'))
        except ValueError as e:
            # Raised in releases <= 3.2 of the plugin (doesn't occur in releases >= 3.3)
            print(e)
        except orthanc.OrthancException as e:
            # Raised in releases >= 3.3 of the plugin (fails with releases <= 3.2)
            print(e)
            print(e.args[0])  # Error code of Orthanc (cf. "orthanc.ErrorCode" enumeration)
            print(e.args[1])  # Description of the error
            print(e.args[0] == orthanc.ErrorCode.UNKNOWN_RESOURCE)  # Returns "True"

orthanc.RegisterOnChangeCallback(OnChange)
