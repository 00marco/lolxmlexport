import asyncio
import json
import logging
import os
import tempfile

from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

from json_schemas import custom_transforms_dict
from xml_transform_utils import XMLTransformUtils


# TODO: write integration test mocking these connections soon
def get_file(filename: str, filepath: str):
    # Blob storage connection string and container name
    connect_str = os.getenv("AzureStorageConnectionString")
    container_name = "xmlexport"
    blob_name = os.path.join(filepath, filename)

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Get the blob client
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    blob_data = blob_client.download_blob().readall()
    return blob_data


# def upload_file(filename: str, filepath: str, data):
#     connect_str = os.getenv("AzureStorageConnectionString")
#     container_name = "xmlexport"
#     blob_name = os.path.join(filepath, filename)

#     # Create the BlobServiceClient object
#     blob_service_client = BlobServiceClient.from_connection_string(connect_str)

#     # Get the blob client
#     blob_client = blob_service_client.get_blob_client(
#         container=container_name, blob=blob_name
#     )

#     blob_client.upload_blob(data, overwrite=True)


async def upload_file(blob_name, data):
    try:
        connection_string = os.getenv("AzureStorageConnectionString")
        container_name = "xmlexport"
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        async with blob_client as bc:
            await bc.upload_blob(data, overwrite=True)
            print(f"Uploaded to blob {blob_client.blob_name}.")
    except Exception as e:
        print(f"Could not upload file: {e}")


async def upload_files_to_blob_storage(input_jsons):
    try:
        # Create tasks for concurrent uploading
        tasks = []
        for input_json in input_jsons:
            input_json = json.loads(input_json)
            xml_output = XMLTransformUtils().json_to_xml(
                json_obj=input_json,
                dict_type="Ingredient",  # TODO infer from schema
                root_name="FormulationML",
                custom_transforms_dict=custom_transforms_dict,
            )
            blob_name = os.path.join(
                "output_ingredient",
                "20240716",  # TODO get somewhere else; maybe another function param
                f"output_{input_json['IngredientCode']}",
            )
            print(blob_name)
            tasks.append(upload_file(blob_name, xml_output))

        print("start tasks")
        # Run tasks concurrently
        await asyncio.gather(*tasks)

        print("All files uploaded successfully.")

    except Exception as e:
        print(f"Could not upload files to blob: {e}")
