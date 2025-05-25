import json
import orthanc
import requests
import requests.auth

COUCHDB_URL = 'http://localhost:5984/'
COUCHDB_USERNAME = 'admin'
COUCHDB_PASSWORD = 'password'
COUCHDB_DATABASE = 'orthanc'

auth = requests.auth.HTTPBasicAuth(COUCHDB_USERNAME, COUCHDB_PASSWORD)

def GetRevision(key):
    # Return the current revision of the document indexed by "key" in the CouchDB database.
    # The value "None" is returned is the document does not exist.
    r = requests.get('%s/%s/%s' % (COUCHDB_URL, COUCHDB_DATABASE, key), auth = auth)
    if r.status_code == 200:
        return r.json() ['_rev']
    else:
        return None

def Store(key, doc):
    # Associate the document "doc" with the provided "key" in the CouchDB database.
    revision = GetRevision(key)

    if revision == None:
        r = requests.put('%s/%s/%s' % (COUCHDB_URL, COUCHDB_DATABASE, key), data = doc, auth = auth)
    else:
        # The key already exists, update its content
        r = requests.put('%s/%s/%s?rev=%s' % (COUCHDB_URL, COUCHDB_DATABASE, key, revision), data = doc, auth = auth)

    r.raise_for_status()

def Delete(key):
    revision = GetRevision(key)
    if revision != None:
        r = requests.delete('%s/%s/%s?rev=%s' % (COUCHDB_URL, COUCHDB_DATABASE, key, revision), auth = auth)
        r.raise_for_status()

def OnChange(changeType, level, resource):
    if changeType == orthanc.ChangeType.NEW_INSTANCE:
        # Once a new DICOM instance is received, store its JSON description into CouchDB
        data = orthanc.RestApiGet('/instances/%s' % resource)
        Store('instance-%s' % resource, data)

        # Then, recursively update its parent series, study, and patient inside CouchDB
        seriesId = json.loads(data) ['ParentSeries']
        data = orthanc.RestApiGet('/series/%s' % seriesId)
        Store('series-%s' % seriesId, data)

        studyId = json.loads(data) ['ParentStudy']
        data = orthanc.RestApiGet('/studies/%s' % studyId)
        Store('study-%s' % studyId, data)

        patientId = json.loads(data) ['ParentPatient']
        data = orthanc.RestApiGet('/patients/%s' % patientId)
        Store('patient-%s' % patientId, data)

    elif changeType == orthanc.ChangeType.DELETED:
        if level == orthanc.ResourceType.INSTANCE:
            Delete('instance-%s' % resource)
        elif level == orthanc.ResourceType.SERIES:
            Delete('series-%s' % resource)
        elif level == orthanc.ResourceType.STUDY:
            Delete('study-%s' % resource)
        elif level == orthanc.ResourceType.PATIENT:
            Delete('patient-%s' % resource)

# Create the CouchDB database
requests.put('%s/%s' % (COUCHDB_URL, COUCHDB_DATABASE), auth = auth)

orthanc.RegisterOnChangeCallback(OnChange)
