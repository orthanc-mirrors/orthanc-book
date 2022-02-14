import orthanc
import threading

TIMER = None

def Hello():
    global TIMER
    TIMER = None
    orthanc.LogWarning("In Hello()")
    # Do stuff...
    TIMER = threading.Timer(1, Hello)  # Re-schedule after 1 second
    TIMER.start()

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.ORTHANC_STARTED:
        orthanc.LogWarning("Starting the scheduler")
        Hello()

    elif changeType == orthanc.ChangeType.ORTHANC_STOPPED:
        if TIMER != None:
            orthanc.LogWarning("Stopping the scheduler")
            TIMER.cancel()

orthanc.RegisterOnChangeCallback(OnChange)
