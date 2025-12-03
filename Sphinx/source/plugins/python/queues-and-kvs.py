import orthanc
import json
import threading
import time


worker_thread = None
is_worker_running = False

def ProcessQueueMessages():
    global is_worker_running

    orthanc.SetCurrentThreadName("QUEUE-PROC")

    while is_worker_running:
        # get messages from the queue named "instances-to-process" that is stored in Orthanc DB.
        # Get the message from the FRONT for FIFO and from the BACK for a LIFO
        # from v7.0, prefer the ReserveQueueValue      message = orthanc.DequeueValue("instances-to-process", orthanc.QueueOrigin.FRONT)
        message, messageId = orthanc.ReserveQueueValue("instances-to-process", orthanc.QueueOrigin.FRONT, 2)

        if message is None:
            # no messages in the queue
            time.sleep(1)
        else:
            payload = json.loads(message.decode('utf-8'))
            resourceId = payload["resource-id"]

            orthanc.LogInfo(f"processing resource {resourceId}")

            # get the value associated to the key resourceId in the "my-store" Key Value Store.
            value = orthanc.GetKeyValue("my-store", resourceId)
            if value is None:
                orthanc.LogWarning(f"no value for this resource: {resourceId}")
            else:
                orthanc.LogInfo(f"Value for resource {resourceId} is {value.decode('utf-8')}")
                orthanc.DeleteKeyValue("my-store", resourceId)

            orthanc.RestApiPut(f"/studies/{payload['study-id']}/labels/{payload['my-data']}", b"")
            # mark the processing as complete (new in v7.0)
            orthanc.AcknowledgeQueueValue("instances-to-process", messageId)


def OnChange(changeType, level, resource: str):
    global worker_thread
    global is_worker_running

    if changeType == orthanc.ChangeType.NEW_INSTANCE:

        processPayload = {
            "resource-id": resource,
            "study-id": json.loads(orthanc.RestApiGet(f"/instances/{resource}/study"))["ID"],
            "my-data": "my-data"
        }

        # Push a message into the queue named "instances-to-process".  It must be a bytes object.
        # The queue is persisted in the Orthanc database and is accessible to all Orthanc instances
        # that are connected to the same database.
        orthanc.EnqueueValue("instances-to-process", json.dumps(processPayload).encode('utf-8'))
        orthanc.LogInfo(f"Enqueued value for resource {resource}")

        # Save information into a store named "my-store".
        # The tuple (store-name, key) must be unique.
        # The value must be a bytes object.
        orthanc.StoreKeyValue("my-store", resource, f"my-data for {resource}".encode('utf-8'))
        orthanc.LogInfo(f"Stored Key-Value for resource {resource}")

    elif changeType == orthanc.ChangeType.ORTHANC_STARTED:

        # start a thread to process the messages from a queue
        worker_thread = threading.Thread(target=ProcessQueueMessages)
        is_worker_running = True
        worker_thread.start()
    
    elif changeType == orthanc.ChangeType.ORTHANC_STOPPED:

        is_worker_running = False
        worker_thread.join()

def OnRestKvsAndQueuesStatistics(output, uri, **request):
    if request['method'] != 'GET':
        output.SendMethodNotAllowed('GET')
    else:
        # show all values in the queue:
        it = orthanc.CreateKeysValuesIterator("my-store")
        values = {}
        while it.Next():
            values[it.GetKey()] = it.GetValue().decode('utf-8')

        statistics = {
            "instances-to-process-size" : orthanc.GetQueueSize("instances-to-process"),
            "my-store-keys-values": values
        }
        output.AnswerBuffer(json.dumps(statistics), 'application/json')

orthanc.RegisterOnChangeCallback(OnChange)
orthanc.RegisterRestCallback('/kvs-queues-statistics', OnRestKvsAndQueuesStatistics)