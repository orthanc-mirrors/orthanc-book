import orthanc
import json

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.NEW_INSTANCE:
        parentSeries = json.loads(orthanc.RestApiGet('/instances/%s/series' % resource))
        
        if parentSeries["MainDicomTags"]["Modality"] == "CR":
            orthanc.LogInfo('Stabilizing CR series directly: %s' % resource)
            ret, hasStableStatusChanged = orthanc.SetStableStatus(parentSeries["ID"], orthanc.StableStatus.STABLE)

orthanc.RegisterOnChangeCallback(OnChange)