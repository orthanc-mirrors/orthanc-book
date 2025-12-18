import json
import orthanc
import os

# Path to the directory containing the DICOM worklists
# https://orthanc.uclouvain.be/hg/orthanc/file/Orthanc-1.11.0/OrthancServer/Plugins/Samples/ModalityWorklists/WorklistsDatabase
WORKLIST_DIR = '/tmp/WorklistsDatabase'

def OnWorklist(answers, query, connection):  # new from v 7.0: issuerAet and calledAet are available from the connection object
    print('Received incoming C-FIND worklist request from %s %s %s:' % (connection.GetConnectionRemoteAet(), connection.GetConnectionRemoteIp(), connection.GetConnectionCalledAet()))

    # old prototype still available
    # def OnWorklist(answers, query, issuerAet, calledAet):
    #     print('Received incoming C-FIND worklist request from %s:' % issuerAet)

    # Get a memory buffer containing the DICOM instance
    dicom = query.WorklistGetDicomQuery()

    # Get the DICOM tags in the JSON format from the binary buffer
    jsonTags = json.loads(orthanc.DicomBufferToJson(
        dicom, orthanc.DicomToJsonFormat.SHORT, orthanc.DicomToJsonFlags.NONE, 0))

    orthanc.LogWarning('C-FIND worklist request to be handled in Python: %s' %
                       json.dumps(jsonTags, indent = 4, sort_keys = True))

    # Loop over the available DICOM worklists
    for path in os.listdir(WORKLIST_DIR):
        if os.path.splitext(path) [1] == '.wl':
            with open(os.path.join(WORKLIST_DIR, path), 'rb') as f:
                content = f.read()
                
                # Test whether the query matches the current worklist
                if query.WorklistIsMatch(content):
                    orthanc.LogWarning('Matching worklist: %s' % path)
                    answers.WorklistAddAnswer(query, content)

orthanc.RegisterWorklistCallback2(OnWorklist)  # new from v 7.0
# orthanc.RegisterWorklistCallback(OnWorklist)
