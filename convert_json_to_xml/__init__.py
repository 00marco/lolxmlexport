import datetime
import json
import logging

import azure.functions as func

from json_schemas import (
    custom_transforms_dict,
)

from xml_transform_utils import XMLTransformUtils


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Main function for the Azure HTTP trigger function.

    This function processes an HTTP request, reads JSON payloads from the request body,
    converts each JSON object to XML using specified transformation rules, and returns
    the XML outputs in the HTTP response.

    Args:
        req (func.HttpRequest): The HTTP request object.

    Returns:
        func.HttpResponse: The HTTP response object containing the XML outputs or an error message.

    Request JSON Schema:
    {
        "type": "object",
        "properties": {
            "input_jsons": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string"
                        },
                        "body": {
                            "type": "object"
                        }
                    },
                    "required": ["key", "body"]
                }
            },
            "input_type": {
                "type": "string",
                "enum": ["Ingredient", "Product"]
            }
        },
        "required": ["input_jsons", "input_type"]
    }
    """
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()
        input_jsons = req_body.get("input_jsons") # list of objects in json
        input_type = req_body.get("input_type") # Ingredient or Product

        xml_outputs = []
        xmlTransformUtils = XMLTransformUtils()
        for input_json in input_jsons:
            xml_output = xmlTransformUtils.json_to_xml(
                json_obj=input_json["body"],
                dict_type=input_type,
                root_name="FormulationML",
                custom_transforms_dict=custom_transforms_dict,
            )
            xml_outputs.append({
                "key": input_json["key"],
                "xml": xml_output
            })
    except Exception as e:
        return func.HttpResponse(
            f"Error: {e}", status_code=400
        )

    return func.HttpResponse(
        json.dumps(xml_outputs),
        status_code=200,
    )
