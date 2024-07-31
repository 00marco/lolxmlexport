import asyncio
import datetime
import json
import logging
import os
import tempfile

import azure.functions as func

# from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from azure.storage.blob.aio import BlobClient, BlobServiceClient, ContainerClient

from ..json_schemas import custom_transforms_dict
from ..storage_utils import get_file
from ..xml_transform_utils import XMLTransformUtils

# async def upload_blob_file(self, blob_service_client: BlobServiceClient, container_name: str):
#     container_client = blob_service_client.get_container_client(container=container_name)
#     with open(file=os.path.join('filepath', 'filename'), mode="rb") as data:
#         blob_client = await container_client.upload_blob(name="sample-blob.txt", data=data, overwrite=True)

# async def async_main(blob_data):
#     # TODO: Replace <storage-account-name> with your actual storage account name
#     account_url = "https://testrbt109238102983.blob.core.windows.net"
#     connection_string = os.getenv("AzureStorageConnectionString")

#     async with BlobServiceClient.from_connection_string(connection_string) as blob_service_client:
#         await blob_data.upload_blob_file(blob_service_client, "xmlexport")


async def convert_and_process_file(input_json_str: str):
    # Convert file
    xmlTransformUtils = XMLTransformUtils()
    input_json = json.loads(input_json_str)
    xml_output = XMLTransformUtils().json_to_xml(
        json_obj=input_json,
        dict_type="Ingredient",  # TODO infer from schema
        root_name="FormulationML",
        custom_transforms_dict=custom_transforms_dict,
    )

    connection_string = os.getenv("AzureStorageConnectionString")
    container_name = "xmlexport"
    async with BlobServiceClient.from_connection_string(
        connection_string
    ) as blob_service_client:
        container_client = blob_service_client.get_container_client(container_name)
        blob_name = os.path.join(
            "output_ingredient_xml",
            "20240716",  # TODO get somewhere else; maybe another function param
            f"output_{input_json['IngredientCode']}.xml",
        )
        blob_client = container_client.get_blob_client(blob_name)

        await blob_client.upload_blob(xml_output, overwrite=True)
        print(f"Uploaded to blob {blob_client.blob_name}.")


async def main(req: func.HttpRequest) -> func.HttpResponse:
    # try:
    logging.info("Python HTTP trigger function processed a request.")

    xml_outputs = []

    input_json_file = get_file(
        filename=req.params["filename"], filepath=req.params["filepath"]
    ).decode("utf-8")

    input_jsons = [x for x in input_json_file.strip().split("\n")]
    tasks = [asyncio.create_task(convert_and_process_file(x)) for x in input_jsons]
    done, pending = await asyncio.wait(tasks)

    return func.HttpResponse(
        json.dumps(xml_outputs),
        status_code=200,
    )
