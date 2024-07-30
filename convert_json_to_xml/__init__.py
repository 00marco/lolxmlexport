import asyncio
import datetime
import json
import logging
import os
import tempfile

import azure.functions as func

from ..json_schemas import custom_transforms_dict
from ..storage_utils import get_file, upload_files_to_blob_storage
from ..xml_transform_utils import XMLTransformUtils


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("Python HTTP trigger function processed a request.")

        xml_outputs = []

        xmlTransformUtils = XMLTransformUtils()
        input_json_file = get_file(
            filename=req.params["filename"], filepath=req.params["filepath"]
        ).decode("utf-8")
    except Exception as e:
        return func.HttpResponse(f"Error: {e}", status_code=400)

    batch = []
    for input_json in [x for x in input_json_file.strip().split("\n")]:
        input_json = json.loads(input_json)
        xml_output = xmlTransformUtils.json_to_xml(
            json_obj=input_json,
            dict_type=req.params["type"],
            root_name="FormulationML",
            custom_transforms_dict=custom_transforms_dict,
        )

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # Write the string content to the temporary file
            tmp_file.write(xml_output.encode())
            # Get the path of the temporary file
            tmp_file_path = tmp_file.name

        batch.append(
            tmp_file_path,
        )
        # return func.HttpResponse(f"Error: {e}", status_code=400)

    try:
        asyncio.run(upload_files_to_blob_storage(batch))
    except Exception as e:
        print("error uploading", e)
    return func.HttpResponse(
        json.dumps(xml_outputs),
        status_code=200,
    )
