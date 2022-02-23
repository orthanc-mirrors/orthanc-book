import json
import orthanc

def Filter(receivedDicom):
    # The list ofvalid status codes for DIMSE C-STORE can be found:
    # https://dicom.nema.org/medical/Dicom/2021e/output/chtml/part04/sect_B.2.3.html

    tags = json.loads(receivedDicom.GetInstanceSimplifiedJson())
    if tags['PatientID'].startswith('001-'):
        # Non-zero return value: The DICOM instance is discarded
        return 0xA900  # DIMSE Failure: Data Set does not match SOP Class
    else:
        return 0  # Success: Accept the DICOM instance

orthanc.RegisterIncomingCStoreInstanceFilter(Filter)
