import os, pathlib, requests

MODEL_BACKEND_ENV = "MODEL_BACKEND"

class ModelInterface:
    def __init__(self):
        backend = os.environ.get(MODEL_BACKEND_ENV, "gpt4all").lower()
        self.backend = backend

        if backend == "gpt4all":
            from gpt4all import GPT4All
            model_path = os.environ.get("OFFLINE_MODEL_NAME")
            if not model_path:
                raise RuntimeError("No OFFLINE_MODEL_NAME provided")
            self.model_path = self.ensure_model(model_path)
            self.model = GPT4All(self.model_path)

        elif backend == "chatgpt":
            import openai
            token = os.environ.get("OPENAI_API_KEY")
            if not token:
                raise RuntimeError("No OPENAI_API_KEY provided")
            openai.api_key = token
            self.openai = openai

        elif backend == "gemini":
            import google.generativeai as genai
            token = os.environ.get("GEMINI_API_KEY")
            if not token:
                raise RuntimeError("No GEMINI_API_KEY provided")
            genai.configure(api_key=token)
            self.model = genai.GenerativeModel("gemini-pro")

        elif backend == "perplexity":
            self.api_token = os.environ.get("PERPLEXITY_API_KEY")
            if not self.api_token:
                raise RuntimeError("No PERPLEXITY_API_KEY provided")

        elif backend == "deepseek":
            self.api_token = os.environ.get("DEEPSEEK_API_KEY")
            if not self.api_token:
                raise RuntimeError("No DEEPSEEK_API_KEY provided")

        else:
            raise RuntimeError(f"Unsupported backend: {backend}")

    def ensure_model(self, model_path: str) -> str:
        path = pathlib.Path(model_path)
        if not path.exists():
            url = os.environ.get("OFFLINE_MODEL_URL")
            if not url:
                raise RuntimeError("No OFFLINE_MODEL_URL provided")
            print(f"Downloading {path.name} from {url}...")
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
        return str(path)

    def run(self, prompt: str) -> str:
        if self.backend == "gpt4all":
            with self.model.chat_session() as session:
                return session.prompt(prompt)

        elif self.backend == "chatgpt":
            resp = self.openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message["content"]

        elif self.backend == "gemini":
            resp = self.model.generate_content(prompt)
            return resp.text

        elif self.backend == "perplexity":
            import requests
            headers = {"Authorization": f"Bearer {self.api_token}"}
            resp = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={"model": "pplx-7b-chat", "messages": [{"role": "user", "content": prompt}]}
            )
            return resp.json()["choices"][0]["message"]["content"]

        elif self.backend == "deepseek":
            import requests
            headers = {"Authorization": f"Bearer {self.api_token}"}
            resp = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
            )
            return resp.json()["choices"][0]["message"]["content"]

        else:
            return f"Unsupported backend: {self.backend}"
