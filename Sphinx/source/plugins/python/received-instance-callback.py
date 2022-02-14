from io import BytesIO

from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike


# from https://pydicom.github.io/pydicom/stable/auto_examples/memory_dataset.html
def write_dataset_to_bytes(dataset):
    with BytesIO() as buffer:
        memory_dataset = DicomFileLike(buffer)
        dcmwrite(memory_dataset, dataset)
        memory_dataset.seek(0)

        return memory_dataset.read()


def ReceivedInstanceCallback(receivedDicom):

    dataset = dcmread(BytesIO(receivedDicom))

    if dataset.PatientID.startswith('001-'):
        return orthanc.ReceivedInstanceCallbackResult.DISCARD, None

    if dataset.PatientID.startswith('002-'):
        return orthanc.ReceivedInstanceCallbackResult.KEEP_AS_IS, None

    dataset.PatientName = str(dataset.PatientName).upper()
    dataset.PatientID = '002-' + dataset.PatientID
    dataset.InstitutionName = "MY INSTITUTION"

    return orthanc.ReceivedInstanceCallbackResult.MODIFIED, write_dataset_to_bytes(dataset)

orthanc.RegisterReceivedInstanceCallback(ReceivedInstanceCallback)
