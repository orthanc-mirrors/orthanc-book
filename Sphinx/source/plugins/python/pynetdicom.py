import json
import orthanc
import pynetdicom

def HandleStore(event):
    orthanc.LogWarning('Handling C-STORE using pynetdicom')
    orthanc.RestApiPost('/instances', event.request.DataSet.getvalue())
    return 0x0000

ae = pynetdicom.AE()
ae.supported_contexts = pynetdicom.AllStoragePresentationContexts

SCP = None

def OnChange(changeType, level, resource):
    global SCP
    
    if changeType == orthanc.ChangeType.ORTHANC_STARTED:
        port = json.loads(orthanc.GetConfiguration()).get('DicomPort', 4242)
        
        SCP = ae.start_server(('', port), block = False, evt_handlers = [
            (pynetdicom.evt.EVT_C_STORE, HandleStore),
        ])
        
        orthanc.LogWarning('DICOM server using pynetdicom has started')

    elif changeType == orthanc.ChangeType.ORTHANC_STOPPED:
        orthanc.LogWarning('Stopping pynetdicom')
        SCP.shutdown()

orthanc.RegisterOnChangeCallback(OnChange)
