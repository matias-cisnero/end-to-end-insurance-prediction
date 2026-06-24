import os
import subprocess
import sys

os.environ["MLFLOW_SERVER_ALLOWED_HOSTS"] = "*"

cmd = [
    sys.executable,
    "-m",
    "mlflow",
    "server",
    "--backend-store-uri",
    "sqlite:///mlflow.db",
    "--default-artifact-root",
    "./mlartifacts",
    "--host",
    "0.0.0.0",
    "--port",
    "5000"
]

try:
    subprocess.run(cmd, check=True)
except KeyboardInterrupt:
    pass
