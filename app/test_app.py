import os
from handle import handle

# Simulate OpenFaaS environment variables

os.environ["OFFLINE_MODEL_NAME"] = "/tmp/mistral-7b-instruct-v0.1.Q4_0.gguf"

os.environ["OFFLINE_MODEL_URL"] = (
    "https://huggingface.co/TheBloke/"
    "Mistral-7B-Instruct-v0.1-GGUF/resolve/main/"
    "mistral-7b-instruct-v0.1.Q4_0.gguf"
)

if __name__ == "__main__":

    print("\n==============================")
    print("LOCAL HANDLE TEST")
    print("==============================\n")

    response = handle("hello")

    print(response)
