import orthanc
import sys

print("sys.path before modification: " + ", ".join(sys.path))

sys.path = ["/usr/lib/python3.8", "/usr/lib/python3.8/lib-dynload", "/tmp/.env/lib/python3.8/site-packages", "/tmp/.venv/lib64/python3.8/site-packages"]

print("sys.path after modification: " + ", ".join(sys.path))

import requests
# ....