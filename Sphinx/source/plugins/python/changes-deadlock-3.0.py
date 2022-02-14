import orthanc
import threading

def OnChange(changeType, level, resource):
    # One can safely invoke the "orthanc" module in this function
    orthanc.LogWarning("Hello world")

def _OnChange(changeType, level, resource):
    # Invoke the actual "OnChange()" function in a separate thread
    t = threading.Timer(0, function = OnChange, args = (changeType, level, resource))
    t.start()

orthanc.RegisterOnChangeCallback(_OnChange)
