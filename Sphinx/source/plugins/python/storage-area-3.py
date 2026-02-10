# Compared to the default Orthanc storage, this storage plugin 
# uses a flat folder structure but prefixes all file paths with 
# the PatientID.  This is a sample only and should not be used 
# in production.

import orthanc
from typing import Tuple, Optional
import json
import os
import re

orthanc_full_configuration = json.loads(orthanc.GetConfiguration())

root_storage_directory = orthanc_full_configuration.get('StorageDirectory', orthanc_full_configuration.get('IndexDirectory', os.curdir))

orthanc.LogWarning(f"Python Storage: root directory: {root_storage_directory}")

def normalize_filename(s: str, replacement_char: str = "_") -> str:
    # Replace invalid characters with the replacement character
    s = re.sub(r'[\\/*?:"<>|]', replacement_char, s)
    # Replace spaces with the replacement character
    s = re.sub(r'\s+', replacement_char, s)
    # Remove leading/trailing replacement characters
    s = s.strip(replacement_char)
    # Ensure the string is not empty
    if not s:
        s = "undefined"
    return s

def get_relative_path(patient_id: str, uuid: str, content_type: orthanc.ContentType) -> str:
    return f"{normalize_filename(patient_id)} - {uuid}{get_extension(content_type)}"

def get_absolute_path(relative_path: str) -> str:
    return os.path.join(root_storage_directory, relative_path)

def get_extension(content_type: orthanc.ContentType):
    if content_type == orthanc.ContentType.DICOM:
        return ".dcm"
    elif content_type == orthanc.ContentType.DICOM_AS_JSON:
        return ".json"
    elif content_type == orthanc.ContentType.DICOM_UNTIL_PIXEL_DATA:
        return ".dcm.head"
    else:
        return ".unk"

def StorageCreate(uuid: str, 
                  content_type: orthanc.ContentType, 
                  compression_type: orthanc.CompressionType, 
                  content: bytes, 
                  dicom_instance: orthanc.DicomInstance) -> Tuple[orthanc.ErrorCode, Optional[bytes]]:
    # orthanc.LogInfo("---- StorageCreate")
    
    instance_tags = json.loads(dicom_instance.GetInstanceJson())
    patient_id = instance_tags["0010,0010"]["Value"]
    try:
        relative_path = get_relative_path(patient_id, uuid, content_type)
        path = get_absolute_path(relative_path)
        with open(path, "wb") as f:
            f.write(content)
        
        # orthanc.LogInfo(f"Successfully created file {path} for {uuid}, wrote {len(content)} bytes")
        str_custom_data = relative_path

        return orthanc.ErrorCode.SUCCESS, str_custom_data.encode('utf-8')
    except IOError as e:
        orthanc.LogError(f"Failed to create storage for {uuid}: {str(e)}")
        return orthanc.ErrorCode.PLUGIN, None
    except Exception as e:
        orthanc.LogError(f"Unexpected error creating storage for {uuid}: {str(e)}")
        return orthanc.ErrorCode.PLUGIN, None

def StorageReadRange(uuid: str, 
                     content_type: orthanc.ContentType, 
                     range_start: int,
                     size: int,
                     custom_data: bytes) -> Tuple[orthanc.ErrorCode, Optional[bytes]]:
    # orthanc.LogInfo("---- StorageReadRange")
    str_custom_data = custom_data.decode('utf-8')
    # orthanc.LogInfo(f"---- CustomData: {str_custom_data}")
    try:
        relative_path = str_custom_data
        path = get_absolute_path(relative_path)

        with open(path, "rb") as f:
            # Move to the start position
            f.seek(range_start)
            # Read the specified number of bytes
            data = f.read(size)
            
        # orthanc.LogInfo(f"Read {len(data)} bytes from position {range_start}")
        return orthanc.ErrorCode.SUCCESS, data
    except FileNotFoundError:
        orthanc.LogError(f"File {path} not found for {uuid}")
        return orthanc.ErrorCode.UNKNOWN_RESOURCE, None
    except Exception as e:
        orthanc.LogError(f"Error reading file {path} for {uuid}: {str(e)}")
        return orthanc.ErrorCode.PLUGIN, None

def StorageRemove(uuid: str,
                  content_type: orthanc.ContentType,
                  custom_data: bytes) -> orthanc.ErrorCode:
    # orthanc.LogInfo("---- StorageRemove")
    
    str_custom_data = custom_data.decode('utf-8')
    # orthanc.LogInfo(f"---- CustomData: {str_custom_data}")
    try:
        relative_path = str_custom_data
        path = get_absolute_path(relative_path)
        if os.path.exists(path):
            os.remove(path)
            # orthanc.LogInfo(f"Successfully removed file {path} for {uuid}")
        else:
            orthanc.LogWarning(f"Storage file not found for removal: {path}")
        
        return orthanc.ErrorCode.SUCCESS
    except IOError as e:
        orthanc.LogError(f"Failed to remove {path} for {uuid}: {str(e)}")
        return orthanc.ErrorCode.PLUGIN
    except Exception as e:
        orthanc.LogError(f"Unexpected error removing {path} for {uuid}: {str(e)}")
        return orthanc.ErrorCode.PLUGIN


orthanc.RegisterStorageArea3(StorageCreate, StorageReadRange, StorageRemove)