import asyncio
import datetime
import json
import logging
import os
import tempfile
from datetime import datetime

import azure.functions as func
from azure.storage.blob import BlobServiceClient as SynchronousBlobServiceClient
from azure.storage.blob.aio import BlobClient, BlobServiceClient, ContainerClient

from ..json_schemas import custom_transforms_dict
from ..xml_transform_utils import XMLTransformUtils


def get_file(filename: str, filepath: str):
    # Blob storage connection string and container name
    connect_str = os.getenv("AzureStorageConnectionString")
    container_name = "xmlexport"
    blob_name = os.path.join(filepath, filename)

    # Create the BlobServiceClient object
    blob_service_client = SynchronousBlobServiceClient.from_connection_string(
        connect_str
    )

    # Get the blob client
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )
    prop = blob_client.get_blob_properties()
    if prop.size > 0:
        blob_data = blob_client.download_blob().readall()
        return blob_data
    else:
        return None


async def convert_and_process_file(
    input_json_str: str, input_file_type: str, input_file_path: str, input_filename: str
):
    # Convert JSON to XML
    xmlTransformUtils = XMLTransformUtils()
    input_json = json.loads(input_json_str)
    xml_output = XMLTransformUtils().json_to_xml(
        json_obj=input_json,
        dict_type=input_file_type,
        root_name="FormulationML",
        custom_transforms_dict=custom_transforms_dict,
    )

    # Upload XML to file
    connection_string = os.getenv("AzureStorageConnectionString")
    container_name = "xmlexport"
    async with BlobServiceClient.from_connection_string(
        connection_string
    ) as blob_service_client:
        container_client = blob_service_client.get_container_client(container_name)
        blob_name = os.path.join(
            input_file_path,
            "xml_files",
            input_filename,
        )
        blob_client = container_client.get_blob_client(blob_name)

        await blob_client.upload_blob(xml_output, overwrite=True)
        logging.debug(f"Uploaded to blob {blob_client.blob_name}.")


async def main(req: func.HttpRequest) -> func.HttpResponse:
    # try:
    logging.debug("Python HTTP trigger function processed a request.")

    input_json_file = get_file(
        filename=req.params["filename"], filepath=req.params["filepath"]
    ).decode("utf-8")
    if not input_json_file:
        return func.HttpResponse(
            f"File is empty.",
            status_code=200,
        )

    input_jsons = [x for x in input_json_file.strip().split("\n") if len(x) > 0]
    tasks = []

    for input_json_str in input_jsons:
        try:
            if not any(
                x
                in [
                    "PlantCode",
                    "IngredientCode",
                    "RecipeCode",
                    "DateCreated",
                ]
                for x in input_json.keys()
            ):
                raise ValueError
            input_json = json.loads(input_json_str)
            input_json_type = req.params["type"]
            plantcode = str(input_json["PlantCode"]).zfill(4)
            if input_json_type == "Ingredient":
                code = input_json["IngredientCode"]
            elif input_json_type == "Product":
                code = input_json["RecipeCode"]
            else:
                raise ValueError

            datetime_str = (
                datetime.strptime(input_json["DateCreated"], "%Y-%m-%d")
                .strftime("%Y-%m-%d %H:%M:%S")
                .replace("-", "")
                .replace(" ", "")
                .replace(":", "")
            )

            input_filename = (
                f"Ration{input_json_type}_{plantcode}_{code}_{datetime_str}.xml"
            )
            tasks.append(
                asyncio.create_task(
                    convert_and_process_file(
                        input_json_str=input_json_str,
                        input_file_type=input_json_type,
                        input_file_path=req.params["filepath"],
                        input_filename=input_filename,
                    )
                )
            )
        except Exception as e:
            logging.debug(
                f"error adding record to task: {e}. input_json: {input_json[:100]}..."
            )
    await asyncio.wait(tasks)

    return func.HttpResponse(
        f"Successfully uploaded {len(input_jsons)} XML files",
        status_code=200,
    )
    # except Exception as e:
    #     return func.HttpResponse(
    #         "There was an error with executing the function",
    #         status_code=500,
    #     )
