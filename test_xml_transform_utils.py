from json_schemas import (
    custom_transforms_dict_ingredient,
    custom_transforms_dict_product,
)
from xml_transform_utils import XMLTransformUtils


class TestXMLTransformUtils:

    def test_json_to_xml(self):
        json_data = {
            "person": {
                "name": "John Doe",
                "age": 30,
                "test": "",
                "address": {"street": "123 Main St", "city": "Anytown"},
            }
        }
        xml_output = XMLTransformUtils().json_to_xml(
            json_obj=json_data,
            dict_type="Product",
            root_name="FormulationML",
            custom_transforms_dict=custom_transforms_dict_product,
        )
        assert (
            xml_output
            == b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<FormulationML xmlns="http://www.formatinternational.com/FormulationML">\n\t<ProductRecipeList>\n\t\t<ProductRecipe>\n\t\t\t<person>\n\t\t\t\t<name>John Doe</name>\n\t\t\t\t<age>30</age>\n\t\t\t\t<test/>\n\t\t\t\t<address>\n\t\t\t\t\t<street>123 Main St</street>\n\t\t\t\t\t<city>Anytown</city>\n\t\t\t\t</address>\n\t\t\t</person>\n\t\t</ProductRecipe>\n\t</ProductRecipeList>\n</FormulationML>\n'
        )
