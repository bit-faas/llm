# 📦 FaaS LLM Repository

## 📌 Overview

This repository provides a standardized template for building and deploying FaaS modules using OpenFaaS with automated CI/CD support.

It ensures consistent structure, automated validation, and seamless deployment across environments.

It also supports offline Large Language Model (LLM) inference using GPT4All, enabling AI-powered functions that run without external API dependencies.

---

## 🎯 Objective

- Ensure all FaaS modules follow a consistent structure  
- Enable automatic testing before merge  
- Support deployment across client machines  
- Simplify scalability and management  
- Provide LLM-backed functions that can run prompts locally using quantized `.gguf` models  

---

## 📂 Repository Structure

```
faas-template/
│
├── build.gradle        → Gradle tasks (build-faas, push-faas, deploy-faas)
├── function.yml        → OpenFaaS configuration
├── deps.gradle         → External dependencies
│
├── src/                → Source code (developer working directory)
│   ├── handler.py      → Includes handle() entrypoint with GPT4All integration
│   ├── handler_test.py
│
├── app/                → Client application using this FaaS module
│
└── README.md
```

Notes:
- `src/handler.py` contains the `handle()` function that accepts a prompt and runs inference with GPT4All  
- `OFFLINE_MODEL_NAME` and `OFFLINE_MODEL_URL` environment variables define which model to use and where to fetch it  
- Models are stored locally for offline execution  

---

## 🛠️ Build Behavior

- A `build/` folder is created during runtime  
- This folder is temporary and used only for build execution  
- It must not be committed to the repository  

.gitignore requirement:
build/

---

## 🔄 Development Flow (CI – Test Server)

1. Developer pushes to `dev` / feature branch  
2. Pull Request created → `main`  
3. Jenkins Test Server is triggered  
4. Build and test execution  
5. On success → reviewer approval  
6. Merge to `main`  

CI Responsibilities:
- Build FaaS module  
- Execute unit tests (`handler_test.py`)  
- Validate functionality before merge  
- Verify LLM integration by running sample prompts against the offline model  

---

## 🚀 Production Flow (CD – Production Server)

1. Code merged to `main`  
2. Production Jenkins triggered  
3. Clean build execution  
4. Test verification  
5. Docker image creation  
6. Push image to registry  
7. On first run, the function downloads the specified `.gguf` model if not already cached  

---

## 📦 Deployment Model

- Docker images are published to a central registry  
- Client systems can:
  - Pull the image  
  - Import into container runtime  
  - Deploy using OpenFaaS  

LLM Support:
- Functions can run prompts locally using GPT4All models  
- No external API calls are required — inference is fully offline  

---

## 🔁 Client Usage

Any client machine with:

- Docker  
- OpenFaaS (faasd)  

Can:

- Pull → Deploy → Invoke function  

This supports:

- Remote execution  
- Multi-device usage (server, desktop, mobile)  
- AI-powered responses via offline LLMs  

---

## 🧪 Testing Strategy

- Test file location: `src/handler_test.py`  

Standard test function:
def test_handle():

Notes:
- Default test is included  
- Developers should extend test cases  
- Tests run automatically during CI  
- LLM tests validate that `handle()` correctly loads the model and returns a response  

---

## 🔗 CI/CD Integration

Integrated with Jenkins pipelines:

Test Pipeline
- Trigger: PR to main  
- Purpose: validation  

Production Pipeline
- Trigger: main branch update  
- Purpose: build and publish  
- Includes validation of LLM model availability  

---

## ⚠️ Guidelines

- Do not modify folder structure  
- Do not commit build artifacts  
- Ensure handler matches `function.yml`  
- Always maintain/update `handler_test.py`  
- Configure `OFFLINE_MODEL_NAME` and `OFFLINE_MODEL_URL` correctly for LLM functions  

---

## 🚀 Future Enhancements

- Version-based deployments  
- Multi-function support  
- Centralized dependency management  
- Automated client updates  
- Support for multiple LLM backends (e.g. Hugging Face Hub, local cache)  

---

## 📝 Notes

This template is designed to:

- Standardize FaaS development  
- Reduce manual deployment effort  
- Enable scalable distributed execution  
- Provide offline AI inference using GPT4All models for robust, self-contained functions  
