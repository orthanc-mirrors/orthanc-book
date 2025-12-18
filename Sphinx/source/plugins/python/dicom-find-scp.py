import json
import orthanc


def OnFind(answers, query, connection):  # new from v 7.0: issuerAet and calledAet are available from the connection object
    print('Received incoming C-FIND request from %s %s %s:' % (connection.GetConnectionRemoteAet(), connection.GetConnectionRemoteIp(), connection.GetConnectionCalledAet()))

    # old prototype still available
    # def OnFindLegacy(answers, query, issuerAet, calledAet):
    #     print('Received incoming C-FIND request from %s:' % issuerAet)

    answer = {}
    for i in range(query.GetFindQuerySize()):
        print('  %s (%04x,%04x) = [%s]' % (query.GetFindQueryTagName(i),
                                           query.GetFindQueryTagGroup(i),
                                           query.GetFindQueryTagElement(i),
                                           query.GetFindQueryValue(i)))
        answer[query.GetFindQueryTagName(i)] = ('HELLO%d-%s' % (i, query.GetFindQueryValue(i)))

    answers.FindAddAnswer(orthanc.CreateDicom(
        json.dumps(answer), None, orthanc.CreateDicomFlags.NONE))

orthanc.RegisterFindCallback2(OnFind)        # new from v 7.0
#orthanc.RegisterFindCallback(OnFindLegacy)  # old version, still available

