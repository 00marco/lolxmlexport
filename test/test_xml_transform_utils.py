import json
import os
import unittest

import azure.functions as func

from ..convert_json_to_xml import main
from ..json_schemas import custom_transforms_dict
from ..xml_transform_utils import XMLTransformUtils


class TestXMLTransformUtils(unittest.TestCase):
    def test_json_to_xml(self):
        json_data = {
            "person": {
                "name": "John Doe",
                "age": 30,
                "test": "",
                "address": {"street": "123 Main St", "city": "Anytown"},
                "testlist": [
                    {"testkey1": {"testkey11": "testkey12"}},
                    {"testkey1": {"testkey11": "testkey12"}},
                    {"testkey2": {"testkey21": "testkey22"}},
                ],
            }
        }
        xml_output = XMLTransformUtils().json_to_xml(
            json_obj=json_data,
            dict_type="Ingredient",
            root_name="FormulationML",
            custom_transforms_dict=custom_transforms_dict,
        )

        with open(os.path.join("test", "test_output.xml"), "r") as file:
            expected_xml = file.read()

        assert xml_output.strip() == expected_xml.strip()

    def test_convert_json_to_xml_endpoint(self):
        # Construct a mock HTTP request.
        req = func.HttpRequest(
            method="GET",
            body=json.dumps(
                {
                    "input_jsons": [
                        {
                            "key": 1,
                            "body": {
                                "person": {
                                    "name": "John Doe",
                                    "age": 30,
                                    "test": "",
                                    "address": {
                                        "street": "123 Main St",
                                        "city": "Anytown",
                                    },
                                    "testlist": [
                                        {"testkey1": {"testkey11": "testkey12"}},
                                        {"testkey1": {"testkey11": "testkey12"}},
                                        {"testkey2": {"testkey21": "testkey22"}},
                                    ],
                                }
                            },
                        },
                        {
                            "key": 2,
                            "body": {
                                "person": {
                                    "name": "John Doe",
                                    "age": 30,
                                    "test": "",
                                    "address": {
                                        "street": "123 Main St",
                                        "city": "Anytown",
                                    },
                                    "testlist": [
                                        {"testkey1": {"testkey11": "testkey12"}},
                                        {"testkey1": {"testkey11": "testkey12"}},
                                        {"testkey2": {"testkey21": "testkey22"}},
                                    ],
                                }
                            },
                        },
                        {
                            "key": 3,
                            "body": {
                                "person": {
                                    "name": "John Doe",
                                    "age": 30,
                                    "test": "",
                                    "address": {
                                        "street": "123 Main St",
                                        "city": "Anytown",
                                    },
                                    "testlist": [
                                        {"testkey1": {"testkey11": "testkey12"}},
                                        {"testkey1": {"testkey11": "testkey12"}},
                                        {"testkey2": {"testkey21": "testkey22"}},
                                    ],
                                }
                            },
                        },
                    ],
                    "input_type": "Ingredient",
                }
            ).encode("utf-8"),
            url="/api/convert_json_to_xml",
        )

        # Call the function.
        resp = main(req)

        print(resp.get_body())
        # Check the output.
        self.assertEqual(
            resp.get_body(),
            b"Test",
        )
