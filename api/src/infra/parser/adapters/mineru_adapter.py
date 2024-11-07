import base64
import json
import os
import subprocess
from domain.entities.raw_document import RawDocument
from ports.parse_to_markdown_port import ParseToMarkdownPort


class MineruAdapter(ParseToMarkdownPort):


    async def parse_to_markdown(self, doc: RawDocument) -> tuple[str, list[str]]:
        # Path to the Python 3.10 executable() env of MinerU and the API script
        python_3_10_executable = "C:/Users/K/miniconda3/envs/MinerU/python.exe"
        api_script = os.path.join("utils", "MinerU_api.py")  # path to api code

        # Encode the PDF bytes in base64 to send to the subprocess
        pdf_bytes_b64 = base64.b64encode(doc.content).decode("utf-8")

        # Prepare input data as JSON to send to the subprocess
        input_data = {"pdf_bytes": pdf_bytes_b64}

        # Run the API script synchronously in a subprocess
        try:
            process = subprocess.run(
                [python_3_10_executable, api_script],
                input=json.dumps(input_data).encode("utf-8"),  # Pass JSON input as UTF-8 encoded bytes
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Decode the stdout and stderr to handle any errors that occurred in the subprocess
            stdout_decoded = process.stdout.decode("utf-8")
            stderr_decoded = process.stderr.decode("utf-8")

            if stderr_decoded:
                print(f"API subprocess: {stderr_decoded}")

            # Parse the output JSON from the API
            # output = json.loads(stdout_decoded)

            # markdown_content = output.get("markdown", "")

            # image_paths = output.get("image_paths", [])

            return stdout_decoded, []

        except Exception as e:
            print(f"An error occurred while processing the PDF: {e}")
            return "", []
