import orthanc
import json

# this plugins provides the same behavior as the default Orthanc implementation

def StorageCommitmentScpCallback(jobId, transactionUid, sopClassUids, sopInstanceUids, remoteAet, calledAet):
    # At the beginning of a Storage Commitment operation, you can build a custom data structure
    # that will be provided as the "data" argument in the StorageCommitmentLookup
    return None


# Reference: `StorageCommitmentScpJob::Lookup` in `OrthancServer/Sources/ServerJobs/StorageCommitmentScpJob.cpp`
def StorageCommitmentLookup(sopClassUid, sopInstanceUid, data):
    success = False
    reason = orthanc.StorageCommitmentFailureReason.NO_SUCH_OBJECT_INSTANCE

    result = json.loads(orthanc.RestApiPost("/tools/lookup", sopInstanceUid))
    if len(result) == 1:
        tags = json.loads(orthanc.RestApiGet(result[0]["Path"] + "/simplified-tags"))
        if all(tag in tags for tag in ["SOPClassUID", "SOPInstanceUID"]) and \
            tags["SOPInstanceUID"] == sopInstanceUid:
            if tags["SOPClassUID"] == sopClassUid:
                success = True
                reason = orthanc.StorageCommitmentFailureReason.SUCCESS
            else:
                # Mismatch in the SOP class UID
                reason = orthanc.StorageCommitmentFailureReason.CLASS_INSTANCE_CONFLICT

    orthanc.LogInfo("  Storage commitment SCP job: " + ("Success" if success else "Failure") + \
                    " while looking for " + sopClassUid + " / " + sopInstanceUid)

    return reason

orthanc.RegisterStorageCommitmentScpCallback(StorageCommitmentScpCallback, StorageCommitmentLookup)