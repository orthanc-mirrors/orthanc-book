import be.uclouvain.orthanc.Callbacks;
import be.uclouvain.orthanc.ChangeType;
import be.uclouvain.orthanc.Functions;
import be.uclouvain.orthanc.ResourceType;
import be.uclouvain.orthanc.KeysValuesIterator;

public class KeyValueStore {
    static {
        // Wait for Orthanc to start so that the database becomes available
        Callbacks.register(new Callbacks.OnChange() {
            @Override
            public void call(ChangeType changeType, ResourceType resourceType, String resourceId) {
                if (changeType == ChangeType.ORTHANC_STARTED) {
                    Functions.storeKeyValue("my_store", "hello", "world".getBytes());
                    System.out.println(new String(Functions.getKeyValue("my_store", "hello")));  // "hello"

                    Functions.storeKeyValue("my_store", "hello2", "world2".getBytes());
                    Functions.storeKeyValue("my_store", "hello3", "world3".getBytes());
                    Functions.storeKeyValue("other_store", "hello4", "world4".getBytes());

                    // Loop over the keys "hello", "hello2", and "hello3"
                    KeysValuesIterator iterator = KeysValuesIterator.createKeysValuesIterator("my_store");
                    while (iterator.next()) {
                        System.out.println(iterator.getKey() + " => " + new String(iterator.getValue()));
                    }

                    Functions.deleteKeyValue("my_store", "hello");
                    System.out.println(Functions.getKeyValue("my_store", "hello"));  // "null"
                }
            }
        });
    }
}
