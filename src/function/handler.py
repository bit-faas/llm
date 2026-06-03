import os
import pathlib
import traceback
import platform
import socket


def handle(prompt: str) -> str:
    try:

        model_name = os.environ.get("OFFLINE_MODEL_NAME")
        model_url = os.environ.get("OFFLINE_MODEL_URL")

        output = []

        output.append("===== LLM FUNCTION DIAGNOSTICS =====")
        output.append("")

        output.append(f"Prompt: {prompt}")
        output.append("")

        output.append("===== ENVIRONMENT =====")
        output.append(f"OFFLINE_MODEL_NAME = {model_name}")
        output.append(f"OFFLINE_MODEL_URL  = {model_url}")
        output.append("")

        output.append("===== PATH CHECK =====")

        if model_name:

            path = pathlib.Path(model_name)

            output.append(f"Configured Path : {path}")
            output.append(f"Parent Directory: {path.parent}")
            output.append(f"File Exists     : {path.exists()}")
            output.append(f"Parent Exists   : {path.parent.exists()}")

            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                output.append("Directory Creation Test : SUCCESS")
            except Exception as e:
                output.append(
                    f"Directory Creation Test : FAILED ({e})"
                )

        else:
            output.append("OFFLINE_MODEL_NAME not set")

        output.append("")

        output.append("===== TMP WRITE TEST =====")

        try:

            test_file = pathlib.Path("/tmp/openfaas_test.txt")

            with open(test_file, "w") as f:
                f.write("openfaas test")

            output.append("Write Test : SUCCESS")

            test_file.unlink()

        except Exception as e:
            output.append(f"Write Test : FAILED ({e})")

        output.append("")

        output.append("===== SYSTEM INFO =====")
        output.append(f"Hostname : {socket.gethostname()}")
        output.append(f"Platform : {platform.platform()}")
        output.append(f"Python   : {platform.python_version()}")
        output.append(f"CWD      : {os.getcwd()}")

        output.append("")
        output.append("===== FUNCTION REACHED SUCCESSFULLY =====")

        return "\n".join(output)

    except Exception as e:

        return f"""
===== UNHANDLED EXCEPTION =====

Type:
{type(e).__name__}

Message:
{str(e)}

Traceback:
{traceback.format_exc()}
"""
