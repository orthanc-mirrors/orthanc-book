import json
import orthanc
import pprint

def OnFind(answers, query, issuerAet, calledAet):
    print('Received incoming C-FIND request from %s:' % issuerAet)

    answer = {}
    for i in range(query.GetFindQuerySize()):
        print('  %s (%04x,%04x) = [%s]' % (query.GetFindQueryTagName(i),
                                           query.GetFindQueryTagGroup(i),
                                           query.GetFindQueryTagElement(i),
                                           query.GetFindQueryValue(i)))
        answer[query.GetFindQueryTagName(i)] = ('HELLO%d-%s' % (i, query.GetFindQueryValue(i)))

    answers.FindAddAnswer(orthanc.CreateDicom(
        json.dumps(answer), None, orthanc.CreateDicomFlags.NONE))

def OnMove(**request):
    orthanc.LogWarning('C-MOVE request to be handled in Python: %s' %
                       json.dumps(request, indent = 4, sort_keys = True))

    # To indicate a failure in the processing, one can raise an exception:
    #   raise Exception('Cannot handle C-MOVE')

orthanc.RegisterFindCallback(OnFind)
orthanc.RegisterMoveCallback(OnMove)
