import sys
import json
import base64
import os

from loguru import logger
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
import magic_pdf.model as model_config

model_config.__use_inside_model__ = True


def process_pdf(pdf_bytes):
    try:
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        # Prepare to write images to a directory
        local_image_dir = os.path.join(current_script_dir, 'images')
        image_writer = DiskReaderWriter(local_image_dir)
        # Prepare the model JSON (empty for built-in model)
        model_json = []
        jso_useful_key = {"_pdf_type": "", "model_list": model_json}

        # Initialize UNIPipe with the PDF bytes
        pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
        pipe.pipe_classify()

        if len(model_json) == 0:
            if model_config.__use_inside_model__:
                pipe.pipe_analyze()
            else:
                logger.error("Need model list input")
                return {"markdown": "", "image_paths": []}

        pipe.pipe_parse()
        markdown_content = pipe.pipe_mk_markdown(str(os.path.basename(local_image_dir)), drop_mode="none")

        # Returning the markdown content and image paths
        return {"markdown": markdown_content,
                "image_paths": []}  # You can modify to return actual image paths if needed

    except Exception as e:
        logger.exception(e)
        return {"markdown": "", "image_paths": []}


if __name__ == "__main__":
    # Read input data from stdin
    input_data = json.loads(sys.stdin.read())
    pdf_bytes_b64 = input_data.get("pdf_bytes")

    if pdf_bytes_b64:
        pdf_bytes = base64.b64decode(pdf_bytes_b64)
        output = process_pdf(pdf_bytes)
        # print(json.dumps(output))
        print(output.get("markdown", ""))
    else:
        print(json.dumps({"markdown": "", "image_paths": []}))
