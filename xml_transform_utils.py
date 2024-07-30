import json
import xml.dom.minidom
import xml.etree.ElementTree as ET

from jsonschema import validate
from jsonschema.exceptions import ValidationError


class XMLTransformUtils:
    def fix_prbasic_timeperiod(self, data: dict) -> dict:
        if list(data.keys()) != ["TimeDescription", "CostList", "Quantity"]:
            raise TypeError

        output = {
            "TimeDescription": data["TimeDescription"],
            "CostList": [x for x in data["CostList"]] + [data["Quantity"]],
        }

        return output

    def get_custom_key(self, input_dict, tag, custom_transforms_dict):
        """
        Find appropriate XML tag in custom_transforms_dict
        """

        for schema in custom_transforms_dict[tag]:
            try:
                validate(instance=input_dict, schema=schema)
                return schema["title"]

            except ValidationError as e:
                print(f"Validation Error: {schema['title']}")

        raise ValueError

    def add_parent_keys_to_dict(self, input_dict: dict, dict_type: str):
        """
        Manually transform input dict
        """

        if dict_type == "Product":
            return {"ProductRecipeList": [{"ProductRecipe": input_dict}]}

        elif dict_type == "Ingredient":
            return {"IngredientList": [{"Ingredient": input_dict}]}
        else:
            raise TypeError

    def indent(self, elem, level=0):
        # Add indentation
        indent_size = "  "
        i = "\n" + level * indent_size
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent_size
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def dict_to_xml(self, tag, d, custom_transforms_dict):
        """
        Helper function to convert a dictionary to XML
        """
        elem = ET.Element(tag)
        if isinstance(d, dict):
            for key, val in d.items():
                child = self.dict_to_xml(key, val, custom_transforms_dict)
                elem.append(child)
        elif isinstance(d, list):
            for item in d:
                if tag in custom_transforms_dict:
                    child = self.dict_to_xml(
                        tag=self.get_custom_key(item, tag, custom_transforms_dict),
                        d=item,
                        custom_transforms_dict=custom_transforms_dict,
                    )
                elif (
                    isinstance(item, dict)
                    and len(item.keys()) == 1
                    and len(item.values()) == 1
                ):  # if list of dictionaries
                    child = self.dict_to_xml(
                        tag=list(item.keys())[0],
                        d=list(item.values())[0],
                        custom_transforms_dict=custom_transforms_dict,
                    )
                else:
                    child = self.dict_to_xml(
                        tag=tag, d=item, custom_transforms_dict=custom_transforms_dict
                    )
                elem.append(child)
        else:
            elem.text = str(d)
        return elem

    def json_to_xml(
        self,
        json_obj: dict,
        dict_type: str,
        root_name: str = "root",
        custom_transforms_dict: dict = {},
        line_padding="",
    ):
        root = self.dict_to_xml(
            root_name,
            self.add_parent_keys_to_dict(json_obj, dict_type),
            custom_transforms_dict,
        )
        root.set("xmlns", "http://www.formatinternational.com/FormulationML")
        # self.indent(root)
        xml_str = ET.tostring(
            root, encoding="unicode", short_empty_elements=False
        ).replace("ns0:", "")
        return xml_str
