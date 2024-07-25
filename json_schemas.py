# if key == tag
# check list of schemas
# if it matches one of them, rename the key to schema title.
# otherwise do nothing
custom_transforms_dict_product = {
    "CostList": [
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "$id": "http://test.com/costlist-cost-schema",
            "title": "Cost",
            "properties": {"CostType": {"type": "string"}, "Value": {"type": "number"}},
            "additionalProperties": True,
        },
        {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "$id": "http://test.com/costlist-quantity-schema",
            "title": "Quantity",
            "properties": {"Units": {"type": "string"}, "Value": {"type": "number"}},
            "additionalProperties": False,
        },
    ],
    "NutrientAnalysisList": {
        "NutrientAnalysis": {
            "NutrientCode": str,
            "NutAnalysis": {"Value": float, "Units": str},
            "LOLDNSNutrientCode": str,
        },
    },
    "IngredientAmountList": {
        "IngredientAmount": {
            "IngredientCode": str,
            "IngredientExtref": int,
            "IngAmount": {"Value": float, "Units": str},
            "LOLSellingPrice": int,
        },
    },
}
{
    "NutrientAnalysis": {
        "NutrientCode": "TOTAL",
        "NutAnalysis": {"Value": 100, "Units": "%"},
        "LOLDNSNutrientCode": "N35",
    }
}

custom_transforms_dict_ingredient = {
    "CostList": {
        "Cost": {"CostType": str, "Value": float},
        "Quantity": {"Value": float, "Units": str},
    },
    "NutrientAnalysisList": {
        "NutrientAnalysis": {
            "NutrientAnalysis": {
                "NutrientCode": str,
                "NutAnalysis": {"Value": int, "Units": str},
                "LOLDNSNutrientCode": str,
            }
        },
    },
    "IngredientAmountList": {
        "IngredientAmount": {
            "IngredientCode": str,
            "IngredientExtref": int,
            "IngAmount": {"Value": float, "Units": str},
            "LOLSellingPrice": int,
        },
    },
}

expected_product_jsonToXML_input = {}
expected_ingredient_jsonToXML_input = {}
