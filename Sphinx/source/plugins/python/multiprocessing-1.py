import math
import orthanc
import time

# CPU-intensive computation taking about 4 seconds
def SlowComputation():
    start = time.time()
    for i in range(1000):
        for j in range(30000):
            math.sqrt(float(j))
    end = time.time()
    duration = (end - start)
    return 'computation done in %.03f seconds\n' % duration

def OnRest(output, uri, **request):
    answer = SlowComputation()
    output.AnswerBuffer(answer, 'text/plain')

orthanc.RegisterRestCallback('/computation', OnRest)
