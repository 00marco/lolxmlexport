import asyncio
import json
import logging
import os
import tempfile

from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient


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


async def upload_file(blob_client, data):
    try:
        async with blob_client as bc:
            await bc.upload_blob(data, overwrite=True)
            print(f"Uploaded to blob {blob_client.blob_name}.")
    except Exception as e:
        print(f"Could not upload file: {e}")


async def upload_files_to_blob_storage(filepaths):
    try:
        connection_string = os.getenv("AzureStorageConnectionString")
        container_name = "xmlexport"
        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        container_client = blob_service_client.get_container_client(container_name)

        # Create tasks for concurrent uploading
        tasks = []
        for tmp_file_path in filepaths:
            with open(tmp_file_path, "r") as file:
                data = file.read()
                blob_name = f"output"
                blob_client = container_client.get_blob_client(blob_name)
                tasks.append(upload_file(blob_client, data["data"]))

        # Run tasks concurrently
        await asyncio.gather(*tasks)

        print("All files uploaded successfully.")

    except Exception as e:
        print(f"Could not upload files to blob: {e}")
