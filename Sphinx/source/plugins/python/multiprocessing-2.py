import math
import multiprocessing
import orthanc
import signal
import time

# CPU-intensive computation taking about 4 seconds
# (same code as above)
def SlowComputation():
    start = time.time()
    for i in range(1000):
        for j in range(30000):
            math.sqrt(float(j))
    end = time.time()
    duration = (end - start)
    return 'computation done in %.03f seconds\n' % duration

# Ignore CTRL+C in the slave processes
def Initializer():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

# Create a pool of 4 slave Python interpreters
POOL = multiprocessing.Pool(4, initializer = Initializer)

def OnRest(output, uri, **request):
    # Offload the call to "SlowComputation" onto one slave process.
    # The GIL is unlocked until the slave sends its answer back.
    answer = POOL.apply(SlowComputation)
    output.AnswerBuffer(answer, 'text/plain')

orthanc.RegisterRestCallback('/computation', OnRest)
