import orthanc
import pprint

def Filter(uri, **request):
    print('User trying to access URI: %s' % uri)
    pprint.pprint(request)
    return True  # False to forbid access

orthanc.RegisterIncomingHttpRequestFilter(Filter)
