import be.uclouvain.orthanc.Callbacks;
import be.uclouvain.orthanc.ChangeType;
import be.uclouvain.orthanc.Functions;
import be.uclouvain.orthanc.ResourceType;

public class Changes {
    static {
        Callbacks.register(new Callbacks.OnChange() {
            @Override
            public void call(ChangeType changeType, ResourceType resourceType, String resourceId) {
                switch (changeType) {
                case ORTHANC_STARTED:
                    Functions.logWarning("Orthanc has started");
                    break;

                case ORTHANC_STOPPED:
                    Functions.logWarning("Orthanc has stopped");
                    break;

                default:
                    break;
                }
            }
        });
    }
}
