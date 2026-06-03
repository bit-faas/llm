# handler.py
from .model_interface import ModelInterface

#  Initialize once at container startup
model = ModelInterface()

def handle(prompt: str) -> str:
    """
    OpenFaaS function entrypoint.
    Uses pre-initialized ModelInterface for inference.
    """
    try:
        return model.run(prompt)
    except Exception as e:
        return f"Error in handle: {str(e)}"

def healthz() -> str:
    # Health check endpoint
    model_path = os.environ.get("OFFLINE_MODEL_NAME")
    if model_path and pathlib.Path(model_path).exists():
        return "OK"
    return "NOT READY"
