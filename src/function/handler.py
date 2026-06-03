import os
import requests
import pathlib
from gpt4all import GPT4All

MODEL_NAME_ENV = "OFFLINE_MODEL_NAME"
MODEL_URL_ENV = "OFFLINE_MODEL_URL"

def ensure_model(model_path: str) -> str:
    """
    Ensure the offline model file exists locally.
    If not, download from OFFLINE_MODEL_URL.
    """
    path = pathlib.Path(model_path)
    if not path.exists():
        url = os.environ.get(MODEL_URL_ENV)
        if not url:
            raise RuntimeError("No OFFLINE_MODEL_URL provided in environment")
        print(f"Downloading {path.name} from {url}...")
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Model download complete.")
    return str(path)


def handle(prompt: str) -> str:
    """
    OpenFaaS function entrypoint.
    Accepts a prompt string, ensures offline model is available,
    and runs inference.
    """
    try:
        model_path = os.environ.get(MODEL_NAME_ENV)
        if not model_path:
            raise RuntimeError("No OFFLINE_MODEL_NAME provided in environment")

        model_path = ensure_model(model_path)

        model = GPT4All(model_path)
        with model.chat_session() as session:
            response = session.prompt(prompt)
        return response

    except Exception as e:
        return f"Error in handle: {str(e)}"
