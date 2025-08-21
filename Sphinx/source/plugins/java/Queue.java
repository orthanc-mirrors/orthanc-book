import be.uclouvain.orthanc.Callbacks;
import be.uclouvain.orthanc.QueueOrigin;
import be.uclouvain.orthanc.ChangeType;
import be.uclouvain.orthanc.Functions;
import be.uclouvain.orthanc.ResourceType;

public class Queue {
    static {
        // Wait for Orthanc to start so that the database becomes available
        Callbacks.register(new Callbacks.OnChange() {
            @Override
            public void call(ChangeType changeType, ResourceType resourceType, String resourceId) {
                if (changeType == ChangeType.ORTHANC_STARTED) {
                    System.out.println(Functions.getQueueSize("my_queue"));   // 0

                    for (int i = 0; i < 5; i++) {
                        Functions.enqueueValue("my_queue", ("hello " + i).getBytes());
                        Functions.enqueueValue("my_queue_2", ("hello " + i).getBytes());
                    }

                    System.out.println(Functions.getQueueSize("my_queue"));   // 5

                    // The following loop will print "hello 0", "hello 1", "hello 2", "hello 3", and "hello 4"
                    for (;;) {
                        byte[] value = Functions.dequeueValue("my_queue", QueueOrigin.FRONT);
                        if (value == null) {
                            break;
                        } else {
                            System.out.println(new String(value));
                        }
                    }

                    // The following loop will print "hello 4", "hello 3", "hello 2", "hello 1", and "hello 0"
                    for (;;) {
                        byte[] value = Functions.dequeueValue("my_queue_2", QueueOrigin.BACK);
                        if (value == null) {
                            break;
                        } else {
                            System.out.println(new String(value));
                        }
                    }
                }
            }
        });
    }
}
