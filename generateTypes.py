import json
import os
from typing import Any, Dict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCHEMA_FILE = os.path.join(BASE_DIR, "graphql.schema.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "SuperNeva/Types.py")

print(OUTPUT_FILE)
print(SCHEMA_FILE)


def load_schema(file_path: str) -> Dict[str, Any]:
    """Load GraphQL schema from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def map_graphql_to_python(type_name: str) -> str:
    """Map GraphQL scalar types to Python types."""
    mappings = {
        "Int": "int",
        "Float": "float",
        "String": "str",
        "Boolean": "bool",
        "ID": "str",
        "Date": "date",
        "JSON": "Any",
    }

    return mappings.get(type_name, type_name)  # Default to custom type


def get_final_type_name(type_info: Dict[str, Any]) -> str:
    """
    Recursively walk down the 'ofType' chain until we get
    to the final GraphQL type that has a non-null 'name'.
    """
    while type_info.get("ofType"):
        type_info = type_info["ofType"]
    return type_info["name"]


def generate_pyi(schema: Dict[str, Any]) -> str:
    """Generate Python type hints from GraphQL schema."""
    output = [
        "from enum import Enum",
        "from datetime import date",
        "from typing import TypedDict, Optional, Any, List\n",
    ]

    types = schema.get("data", {}).get("__schema", {}).get("types", [])

    for gql_type in types:
        kind = gql_type["kind"]
        name = gql_type["name"]

        if kind == "INPUT_OBJECT" and not name.startswith("__"):
            output.append(f"class {name}(TypedDict, total=False):")

            for field in gql_type.get("inputFields", []):
                field_name = field["name"]

                # If the field is a LIST
                if field["type"]["kind"] == "LIST":
                    final_name = get_final_type_name(field["type"]["ofType"])
                    base_type = map_graphql_to_python(final_name)
                    # e.g. 'targets: Optional[List["str"]]'
                    line = f'    {field_name}: Optional[List["{base_type}"]]'
                else:
                    final_name = get_final_type_name(field["type"])
                    base_type = map_graphql_to_python(final_name)
                    # e.g. 'description: Optional["MLStringInput"]'
                    line = f'    {field_name}: Optional["{base_type}"]'

                # Avoid Python keyword conflicts
                if field_name == "from":
                    field_name = f"__{field_name}"
                    # We need to update `line` so it uses the new field_name
                    if field["type"]["kind"] == "LIST":
                        line = f'    {field_name}: Optional[List["{base_type}"]]'
                    else:
                        line = f'    {field_name}: Optional["{base_type}"]'

                output.append(line)

            output.append("")

        elif kind == "OBJECT" and not name.startswith("__"):
            if name == "Mutation":
                continue
            if name == "Query":
                continue
            if name == "Subscription":
                continue
            output.append(f"class {name}(TypedDict, total=False):")
            for field in gql_type.get("fields", []):
                field_name = field["name"]
                if field_name == "from":
                    field_name = f"__{field_name}"
                # handle list type
                if field["type"]["kind"] == "LIST":
                    if field["type"]["ofType"]["kind"] == "NON_NULL":
                        field_type = map_graphql_to_python(
                            field["type"]["ofType"]["ofType"]["name"]
                        )
                    else:
                        field_type = map_graphql_to_python(
                            field["type"]["ofType"]["name"]
                        )
                    output.append(f'    {field_name}: Optional[List["{field_type}"]]')
                else:
                    field_type = map_graphql_to_python(field["type"]["name"])
                    output.append(f'    {field_name}: Optional["{field_type}"]')

            output.append("")

        elif kind == "ENUM":
            if name.startswith("__"):
                """Do nothing"""
            else:
                output.append(f"class {name}(str, Enum):")
                for enum_value in gql_type.get("enumValues", []):
                    output.append(f'    {enum_value["name"]} = "{enum_value["name"]}"')
                output.append("")

        elif kind == "SCALAR":
            if name not in ("Int", "Float", "String", "Boolean", "ID"):
                output.append(f"{name} = Any")

        elif kind == "UNION":
            output.append(f"{name} = Any")
            output.append("")

    return "\n".join(output)


def save_pyi_file(content: str, file_path: str) -> None:
    """Save generated type hints to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    schema = load_schema(SCHEMA_FILE)
    pyi_content = generate_pyi(schema)
    save_pyi_file(pyi_content, OUTPUT_FILE)
    print(f"Type hints generated in {OUTPUT_FILE}")

# import json
# import os
# from typing import Any, Dict

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SCHEMA_FILE = os.path.join(BASE_DIR, "graphql.schema.json")
# OUTPUT_FILE = os.path.join(BASE_DIR, "SuperNeva/Types.py")

# print(OUTPUT_FILE)
# print(SCHEMA_FILE)


# def load_schema(file_path: str) -> Dict[str, Any]:
#     """Load GraphQL schema from a JSON file."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)


# def map_graphql_to_python(type_name: str) -> str:
#     """
#     Map GraphQL scalar types to Python types.
#     Eğer type_name tanınmıyorsa varsayılan olarak 'str' döndürür.
#     (Örn. 'MLStringInput' gibi custom adlar => 'MLStringInput'
#      SCALAR olmayan adlar => typed dict adında gelebilir.)
#     """
#     mappings = {
#         "Int": "int",
#         "Float": "float",
#         "String": "str",
#         "Boolean": "bool",
#         "ID": "str",
#         "Date": "date",
#         "JSON": "Any",
#     }
#     # Eğer tanımlanmamışsa fallback = kendisi
#     # (INPUT_OBJECT ya da OBJECT adları typed dict’e karşılık geliyor olabilir),
#     # ama SCALAR ismi de olabilir. Onu bir alt fonksiyon handle edecek.
#     return mappings.get(type_name, type_name if type_name else "Any")


# def format_type_reference(type_info: Dict[str, Any], is_optional: bool = True) -> str:
#     """
#     Bu fonksiyon, GraphQL tip tanımını (kind: SCALAR, NON_NULL, LIST, INPUT_OBJECT, vb.)
#     Python typed dict alanı için uygun type string'ine dönüştürür.

#     - NON_NULL => is_optional=False (iç tip opsiyonel olmayacak)
#     - LIST => `List[...]`, eğer opsiyonel ise `Optional[List[...]]`
#     - SCALAR / INPUT_OBJECT / OBJECT / ENUM => map_graphql_to_python() ile
#       'str', 'bool', 'SomeCustomType' vs. dönebilir.
#       Opsiyonel ise `Optional["..."]`, değilse `"..."`
#     """
#     kind = type_info.get("kind")

#     if kind == "NON_NULL":
#         # Non-null => opsiyonel değil
#         return format_type_reference(type_info["ofType"], is_optional=False)

#     elif kind == "LIST":
#         # Liste
#         # ofType => iç tipi özyinelemeli parse edelim
#         inner = format_type_reference(type_info["ofType"], is_optional=True)
#         # List => eğer is_optional=True => Optional[List[inner]]
#         list_str = f"List[{inner}]"
#         if is_optional:
#             return f"Optional[{list_str}]"
#         else:
#             return list_str

#     else:
#         # SCALAR, INPUT_OBJECT, ENUM, vb.
#         # Adını map_graphql_to_python ile dönüştür (ör. "String" => "str",
#         # "MLStringInput" => "MLStringInput" eğer mappings'te yoksa)
#         name = type_info.get("name") or "Any"
#         pytype = map_graphql_to_python(name)
#         # typed dict'te "Optional[...]" ya da sadece "..."
#         if is_optional:
#             return f'Optional["{pytype}"]'
#         else:
#             return f'"{pytype}"'


# def generate_pyi(schema: Dict[str, Any]) -> str:
#     """Generate Python type hints from GraphQL schema."""
#     output = [
#         "from enum import Enum",
#         "from datetime import date",
#         "from typing import TypedDict, Optional, Any, List",
#         "",
#     ]

#     types = schema.get("data", {}).get("__schema", {}).get("types", [])

#     for gql_type in types:
#         kind = gql_type["kind"]
#         name = gql_type["name"]

#         # Skip __types
#         if name.startswith("__"):
#             continue

#         if kind == "INPUT_OBJECT":
#             # Ör: inputFields => typed dict alanları
#             output.append(f"class {name}(TypedDict, total=False):")
#             for field in gql_type.get("inputFields", []):
#                 field_name = field["name"]
#                 # Python'da 'from' rezerve kelime
#                 if field_name == "from":
#                     field_name = "__from"

#                 # parse tip
#                 field_type_str = format_type_reference(field["type"], is_optional=True)
#                 output.append(f"    {field_name}: {field_type_str}")
#             output.append("")

#         elif kind == "OBJECT":
#             # Ör: normal type (Query/Mutation/Subscription hariç)
#             if name in ("Mutation", "Query", "Subscription"):
#                 continue

#             output.append(f"class {name}(TypedDict, total=False):")
#             for field in gql_type.get("fields", []):
#                 field_name = field["name"]
#                 if field_name == "from":
#                     field_name = "__from"

#                 field_type_str = format_type_reference(field["type"], is_optional=True)
#                 output.append(f"    {field_name}: {field_type_str}")
#             output.append("")

#         elif kind == "ENUM":
#             if name.startswith("__"):
#                 """Do nothing"""
#             else:
#                 output.append(f"class {name}(str, Enum):")
#                 for enum_value in gql_type.get("enumValues", []):
#                     output.append(f'    {enum_value["name"]} = "{enum_value["name"]}"')
#                 output.append("")

#         elif kind == "SCALAR":
#             if name not in ("Int", "Float", "String", "Boolean", "ID"):

#                 output.append(f"{name} = Any")
#                 output.append("")

#         elif kind == "UNION":
#             output.append(f"{name} = Any")
#             output.append("")

#     return "\n".join(output)


# def save_pyi_file(content: str, file_path: str) -> None:
#     """Save generated type hints to a file."""
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(content)


# if __name__ == "__main__":
#     schema = load_schema(SCHEMA_FILE)
#     pyi_content = generate_pyi(schema)
#     save_pyi_file(pyi_content, OUTPUT_FILE)
#     print(f"Type hints generated in {OUTPUT_FILE}")
