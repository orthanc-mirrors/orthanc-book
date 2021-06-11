import json
import orthanc

# Create a dictionary mapping the numeric values in enumeration
# "orthanc.ValueRepresentation" to the name of the corresponding VR
VR_NAMES = {}
for name in dir(orthanc.ValueRepresentation):
    if not name.startswith('_'):
        value = getattr(orthanc.ValueRepresentation, name)
        VR_NAMES[value] = name

entry = orthanc.LookupDictionary('PatientID')

orthanc.LogWarning('Entry in the dictionary: %s' %
                   json.dumps(entry, indent = 4, sort_keys = True))

orthanc.LogWarning('Name of the value representation: %s' %
                   VR_NAMES[entry['ValueRepresentation']])
