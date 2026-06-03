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
