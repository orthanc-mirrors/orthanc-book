import json
import orthanc
import pprint

def OnMoveBasic(**request):
    orthanc.LogWarning('C-MOVE request to be handled in Python: %s' %
                       json.dumps(request, indent = 4, sort_keys = True))

    # The C-MOVE request above would print the following information in the
    # Orthanc logs::

    #   W0610 18:30:36.840865 PluginsManager.cpp:168] C-MOVE request to be handled in Python: {
    #       "AccessionNumber": "", 
    #       "Level": "INSTANCE", 
    #       "OriginatorAET": "MOVESCU", 
    #       "OriginatorID": 1, 
    #       "PatientID": "", 
    #       "SOPInstanceUID": "", 
    #       "SeriesInstanceUID": "", 
    #       "SourceAET": "SOURCE", 
    #       "StudyInstanceUID": "1.2.3.4", 
    #       "TargetAET": "TARGET"
    #   }

    # To indicate a failure in the processing, one can raise an exception:
    #   raise Exception('Cannot handle C-MOVE')

    # It is now up to your Python callback to process the C-MOVE SCU request,
    # for instance by calling the route /modalities/{...}/store.


# More advanced Move driver, providing progress reporting to the MOVE SCU originator and
# providing more information about the DicomConnection.  
# For a full sample, see https://github.com/orthanc-team/dicom-dicomweb-proxy/blob/main/proxy.py
class MoveDriver:

    def __init__(self, request, connection) -> None:
        self.request = request  # dictionnary containing the C-MOVE request e.g: {
        #       "AccessionNumber": "", 
        #       "Level": "INSTANCE", 
        #       "OriginatorID": 1, 
        #       "PatientID": "", 
        #       "SOPInstanceUID": "", 
        #       "SeriesInstanceUID": "", 
        #       "StudyInstanceUID": "1.2.3.4",
        #       "TargetAET": "TARGET"
        #   }

        # connection.GetConnectionCalledAet()  is equivalent to request["SourceAET"] in older versions of the callback
        # connection.GetConnectionRemoteAet()  is equivalent to request["OriginatorAET"] in older versions of the callback
        # connection.GetConnectionRemoteIp()   is new in v 7.0

        self.instances_ids_to_transfer = [] # TODO: build a list of instances to transfer from the query
        self.instance_counter = 0


def CreateMoveCallback(connection, **request):  # from v 7.0; to use with orthanc.RegisterMoveCallback3()
    # simply create the move driver object now and return it to Orthanc
    orthanc.LogInfo("CreateMoveCallback")
    driver = MoveDriver(request=request, connection=connection)
    return driver

def GetMoveSizeCallback(driver: MoveDriver):
    # query the remote server to list and count the instances to retrieve
    orthanc.LogInfo("GetMoveSizeCallback")
    return len(driver.instances_ids_to_transfer)

def ApplyMoveCallback(driver: MoveDriver):
    # move one instance at a time
    orthanc.LogInfo("ApplyMoveCallback")
    instance_id = driver.instances_ids_to_transfer[driver.instance_counter]
    driver.instance_counter += 1
    # TODO store the instance in the destination
    return orthanc.ErrorCode.SUCCESS

def FreeMoveCallback(driver):
    # free the resources that have been allocated by the move driver - if any
    orthanc.LogInfo("FreeMoveCallback")
    

orthanc.RegisterMoveCallback3(CreateMoveCallback, GetMoveSizeCallback, ApplyMoveCallback, FreeMoveCallback)
# orthanc.RegisterMoveCallback(OnMoveBasic)
