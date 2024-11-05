from io import BytesIO
import PyPDF2
import os
import json
import base64
import subprocess

from domain.entities.raw_document import RawDocument

class Parser:
    @staticmethod
    def parse_to_text(content: bytes) -> tuple[str, list[str]]:
        reader = PyPDF2.PdfReader(BytesIO(content))
        pages_text = []

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            if text:
                pages_text.append(text)

        return "\n".join(pages_text), pages_text

    @staticmethod
    async def parse_to_markdown(doc: RawDocument) -> tuple[str, list[str]]:



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
            #output = json.loads(stdout_decoded)

            #markdown_content = output.get("markdown", "")

            #image_paths = output.get("image_paths", [])


            return stdout_decoded, []

        except Exception as e:
            print(f"An error occurred while processing the PDF: {e}")
            return "", []
