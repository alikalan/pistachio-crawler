
import os

URL = os.getenv("URL")

if os.getenv("RUN_ENV") == "docker":
    CHROMEPATH = os.getenv("DOCKER_CHROMEPATH")
else:
    CHROMEPATH = os.getenv("LOCAL_CHROMEPATH")
