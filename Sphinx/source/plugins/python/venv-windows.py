import orthanc
import sys

print("sys.path before modification: " + ", ".join(sys.path))

sys.path.insert(0, "C:/tmp/.venv/Lib/site-packages")

print("sys.path after modification: " + ", ".join(sys.path))

import requests
# ....
