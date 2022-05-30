import json
import orthanc


# this script accepts 3 instances from STORESCU and then, rejects the next ones

storeScuInstanceCounter = 0

def FilterIncomingCStoreInstance(receivedDicom):
    # The list ofvalid status codes for DIMSE C-STORE can be found:
    # https://dicom.nema.org/medical/Dicom/2021e/output/chtml/part04/sect_B.2.3.html

    global storeScuInstanceCounter

    origin = receivedDicom.GetInstanceOrigin()

    if origin == orthanc.InstanceOrigin.DICOM_PROTOCOL:  # should always be true in the CStore callback !

        remoteAet = receivedDicom.GetInstanceRemoteAet()
        
        if remoteAet == "STORESCU":
            storeScuInstanceCounter += 1

        if storeScuInstanceCounter > 3:
            # Non-zero return value: The DICOM instance is discarded
            return 0xA700
    
    return 0  # Success: Accept the DICOM instance

orthanc.RegisterIncomingCStoreInstanceFilter(FilterIncomingCStoreInstance)
