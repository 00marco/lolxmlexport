from ..json_schemas import (
    custom_transforms_dict_ingredient,
    custom_transforms_dict_product,
)
from ..xml_transform_utils import XMLTransformUtils
import os


class TestXMLTransformUtils:
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
            custom_transforms_dict=custom_transforms_dict_product,
        )

        with open(os.path.join("test", "test_output.xml"), "r") as file:
            expected_xml = file.read()

        assert xml_output.strip() == expected_xml.strip()
