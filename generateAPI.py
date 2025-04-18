# import json
# import os
# from typing import Any, Dict, List, Optional

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SCHEMA_FILE = os.path.join(BASE_DIR, "graphql.schema.json")
# OUTPUT_FILE = os.path.join(BASE_DIR, "SuperNeva/SuperNevaAPI.py")
# ENDPOINT_MAPPING_FILE = os.path.join(BASE_DIR, "endpoints.json")

# print(OUTPUT_FILE)
# print(SCHEMA_FILE)


# def load_schema(file_path: str) -> Dict[str, Any]:
#     """Belirtilen dosyadan JSON şemasını yükler."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)


# def cleanup_null_dict_values(d: Dict[str, Any]) -> Dict[str, Any]:
#     return {k: v for k, v in d.items() if v is not None}


# def map_graphql_to_python(type_name: str) -> str:
#     """
#     GraphQL scalar tiplerini Python tiplerine dönüştürür.
#     Eğer tip ismi tanınmıyorsa (ör. "promptId", "skip") -> "str" olarak dön.
#     """
#     # Tanınan scalars
#     mappings = {
#         "Int": "int",
#         "Float": "float",
#         "String": "str",
#         "Boolean": "bool",
#         "ID": "str",
#         "Date": "date",
#         "JSON": "Any",
#     }
#     return mappings.get(type_name, type_name or "str")  # default fallback => "str"


# # ------------------- DATA STRUCTURES -------------------
# class EndpointDef:
#     """
#     Bir endpoint fonksiyonunu temsil eder.
#     Ek Özellikler:
#       ignore_args (List[str]): Bu parametreler GraphQL arg'lardan ve body'den atılacak.
#       no_body (bool): true ise, request'e body={} gönderilir (body parametresi "false" ise).
#     """

#     def __init__(
#         self,
#         name: str,
#         method: str,
#         path: str,
#         gql_type: str,
#         ignore_args: List[str],
#         no_body: bool,
#     ):
#         self.name = name
#         self.method = method
#         self.path = path
#         self.gql_type = gql_type
#         self.ignore_args = ignore_args
#         self.no_body = no_body  # True => body={}


# class Node:
#     """
#     Her Node, tek bir sınıfı temsil eder.
#     - path_tokens: ['Accounts','me','collections'] => class_name: "AccountsMeCollections"
#     - method_name: Ebeveynin ctor'unda self.<method_name> = <class_name>(...) => "collections"
#     - endpoints: Bu node'a ait fonksiyon tanımları (EndpointDef listesi)
#     - children: Alt Node listesi
#     """

#     def __init__(self, path_tokens: List[str], method_name: str):
#         self.path_tokens = path_tokens
#         self.method_name = method_name
#         self.class_name = "".join(token.capitalize() for token in path_tokens if token)
#         self.endpoints: List[EndpointDef] = []
#         self.children: List["Node"] = []


# # ------------------- PARSE MAPPING -------------------
# def build_tree_from_mapping(mapping: Dict[str, Any]) -> List[Node]:
#     """endpointMapping'in top-level key'leri için kök Node'lar oluştur."""
#     roots: List[Node] = []
#     for top_key, items in mapping.items():
#         root_node = Node([top_key], method_name=top_key.lower())
#         parse_items(items, root_node)
#         roots.append(root_node)
#     return roots


# def parse_items(items: Any, parent: Node):
#     """items genellikle list olur. Her elemanı parse_item'e gönderir."""
#     if isinstance(items, list):
#         for it in items:  # type: ignore
#             parse_item(it, parent)  # type: ignore
#     elif isinstance(items, dict):
#         parse_item(items, parent)  # type: ignore
#     else:
#         pass


# def parse_item(item: Dict[str, Any], parent: Node):
#     """
#     Bir item inceler:
#       - "method","name","path","type" => endpoint
#       - "ignoreArgs", "body" => ek parametreler
#       - "endpoints" => alt resource
#     """
#     has_endpoint_fields = all(k in item for k in ("method", "name", "path", "type"))
#     endpoints_data = item.get("endpoints")
#     method_val = item.get("method") or ""
#     name_val = item.get("name") or ""
#     path_val = item.get("path") or ""
#     gql_type = item.get("type") or ""

#     # ignoreArgs ve body
#     ignore_args: List[str] = item.get("ignoreArgs", [])
#     body_param = item.get("body", True)  # default True => normal body
#     no_body = body_param is False

#     # "pass-through" check:
#     if not method_val and not name_val and endpoints_data:
#         # sadece alt endpoints var => parent'a ekle
#         parse_items(endpoints_data, parent)
#         return

#     # alt "endpoints" var => child node
#     if endpoints_data and isinstance(endpoints_data, list):
#         seg = method_val or name_val or "unknown"
#         child_node = Node(parent.path_tokens + [seg], method_name=seg)

#         # eğer bu item aynı zamanda endpoint parametrelerine de sahipse => ekle
#         if has_endpoint_fields:
#             ep = EndpointDef(
#                 name_val, method_val, path_val, gql_type, ignore_args, no_body
#             )
#             child_node.endpoints.append(ep)

#         parse_items(endpoints_data, child_node)
#         parent.children.append(child_node)
#     else:
#         # leaf endpoint => direkt parent'a ekle
#         if has_endpoint_fields:
#             ep = EndpointDef(
#                 name_val, method_val, path_val, gql_type, ignore_args, no_body
#             )
#             parent.endpoints.append(ep)


# # ------------------- GRAPHQL HELPER -------------------
# def get_graphql_field(
#     schema_types: List[Dict[str, Any]], gql_type: str, gql_name: str
# ) -> Dict[str, Any]:
#     """
#     GraphQL tip listesi içinde gql_type ("Query","Mutation" vs.), fields içinde gql_name'i döndür.
#     Yoksa {}
#     """
#     tdef = next((t for t in schema_types if t["name"] == gql_type), None)
#     if not tdef:
#         return {}
#     fields = tdef.get("fields", [])
#     return next((f for f in fields if f["name"] == gql_name), {})  # type: ignore


# def resolve_arg_import_type(argdef: Dict[str, Any]) -> Optional[str]:
#     """
#     Arg definition'ının import tipini döndürür.
#     """
#     type = argdef.get("type", {})
#     if type.get("kind") == "NON_NULL":
#         type = type.get("ofType", {})
#         if type.get("kind") == "LIST":
#             type = type.get("ofType", {})
#             if type.get("kind") == "NON_NULL":
#                 type = type.get("ofType", {})
#     if type.get("kind") == "LIST":
#         type = type.get("ofType", {})
#         if type.get("kind") == "NON_NULL":
#             type = type.get("ofType", {})
#     if type.get("kind") == "SCALAR":
#         return None
#     return type.get("name", "Any")


# def map_graphql_arg_type(arg_def: Dict[str, Any]) -> str:
#     """
#     Maps GraphQL type definitions to Python type hints recursively.
#     Handles nested NON_NULL and LIST types.
#     Returns Python type hints like: str, Optional[str], List[str], Optional[List[str]], etc.
#     """

#     def handle_type(type_def: Dict[str, Any], inside_list: bool = False) -> str:
#         if not type_def:
#             return '"Any"'

#         kind = type_def.get("kind")
#         name = type_def.get("name")
#         of_type = type_def.get("ofType", {})

#         if kind == "NON_NULL":
#             inner = handle_type(of_type, inside_list)
#             # If we're inside a list, just return the inner type without Optional
#             # If not, strip Optional if it exists
#             if inside_list:
#                 return inner
#             if inner.startswith("Optional["):
#                 return inner[9:-1]
#             if inner.startswith('"') and inner.endswith('"'):
#                 return inner[1:-1]
#             return inner
#         elif kind == "LIST":
#             # Pass inside_list=True to handle_type for list elements
#             inner_type = handle_type(of_type, True)
#             return f"Optional[List[{inner_type}]]"
#         elif name:
#             # Only wrap in Optional if not inside a list
#             mapped_type = map_graphql_to_python(name)
#             return (
#                 f'Optional["{mapped_type}"]' if not inside_list else f'"{mapped_type}"'
#             )
#         else:
#             return '"Any"'

#     # Start with the top-level type
#     type_def = arg_def.get("type", {})
#     result = handle_type(type_def)

#     return result


# def extract_path_params(path_str: str) -> List[str]:
#     """
#     /accounts/me/states/:stateId => ["stateId"]
#     /some/:a/plus/:b => ["a","b"]
#     """
#     parts = path_str.split("/")
#     return [seg[1:] for seg in parts if seg.startswith(":") and len(seg) > 1]


# def build_fstring_path(path_str: str, path_params: List[str]) -> str:
#     """
#     :xyz -> {xyz} + f""
#     """
#     new_path = path_str
#     for param in path_params:
#         new_path = new_path.replace(f":{param}", f"{{{param}}}")
#     return f'f"{new_path}"'


# # ------------------- FALLBACK ARGS (ör. list) -------------------
# def fallback_args_if_not_found(method_name: str) -> List[Dict[str, Any]]:
#     """
#     Eğer GraphQL'de field yoksa ve method 'list' ise => ek parametreler
#     """
#     if method_name == "list":
#         # _id, limit, skip, sort, filters => SCALAR => "str"
#         def mkarg(nm: str):
#             return {"name": nm, "type": {"kind": "SCALAR", "name": "String"}}

#         return [
#             mkarg("_id"),
#             mkarg("limit"),
#             mkarg("skip"),
#             mkarg("sort"),
#             mkarg("filters"),
#         ]
#     return []


# # ------------------- CODE GENERATION -------------------
# def generate_code(roots: List[Node], schema_types: List[Dict[str, Any]]) -> str:
#     """
#     BFS sırayla: Node -> class
#     Each Node => class <class_name>(SNRequest):
#         def __init__(...):
#             super().__init__(*args, **kwargs)
#             self.<childName> = <childClass>(...)
#         def <endpoint_method>(...):
#             ...
#     """
#     from collections import deque

#     lines: List[str] = []
#     import_types: List[str] = []
#     visited: set[str] = set()
#     queue = deque(roots)

#     while queue:
#         node = queue.popleft()
#         if node.class_name in visited:
#             continue
#         visited.add(node.class_name)

#         for child in node.children:
#             queue.append(child)

#         # Sınıf başlığı
#         lines.append(f"class SN{node.class_name}(SNRequest):")
#         lines.append("    def __init__(self, *args: Any, **kwargs: Any) -> None:")
#         lines.append("        super().__init__(*args, **kwargs)")

#         # Alt node referansları
#         for c in node.children:
#             lines.append(
#                 f"        self.{c.method_name} = SN{c.class_name}(*args, **kwargs)"
#             )
#         lines.append("")

#         # Endpoint metodları
#         for ep in node.endpoints:
#             # GraphQL field
#             gql_field = get_graphql_field(schema_types, ep.gql_type, ep.name)
#             if not gql_field:
#                 # fallback (örneğin method=='list')
#                 fallback = fallback_args_if_not_found(ep.method)
#                 gql_field = {"args": fallback, "type": {"name": "Any"}}

#             ret_type = gql_field.get("type", {}).get("name", "Any")  # type: ignore
#             if (
#                 ret_type
#                 and ret_type not in ("Any", "")
#                 and ret_type not in import_types
#             ):
#                 import_types.append(ret_type)  # type: ignore

#             field_args: List[Dict[str, Any]] | Any = gql_field.get("args", [])

#             # Path param analizi
#             path_params = extract_path_params(ep.path)
#             path_params_set = set(path_params)

#             arg_list: List[str] = []
#             body_list: List[str] = []

#             for argdef in field_args:
#                 arg_name = argdef["name"]  # type: ignore
#                 if arg_name in ep.ignore_args:
#                     # Bu parametre ignoreArgs'ta => yok say
#                     continue
#                 pytype = map_graphql_arg_type(argdef)  # type: ignore

#                 if argdef is not None:
#                     import_type = resolve_arg_import_type(argdef)
#                     if import_type is not None:
#                         import_types.append(import_type)

#                 # print(pytype, arg_name)
#                 # import_types.append(pytype)
#                 # path param?
#                 if arg_name in path_params_set:
#                     # method imzasına ekle, body'ye koyma
#                     arg_list.append(f"{arg_name}: {pytype}")
#                 else:
#                     # normal param
#                     arg_list.append(f"{arg_name}: {pytype}")
#                     # body=true ise => body'ye ekle
#                     if not ep.no_body:
#                         body_list.append(f'"{arg_name}": {arg_name}')

#             # method signature
#             if arg_list:
#                 signature_args = ", ".join(arg_list) + ", _auth: Optional[Auth] = None"
#             else:
#                 signature_args = "_auth: Optional[Auth] = None"

#             lines.append(f"    def {ep.method}(self, {signature_args}) -> {ret_type}:")

#             # path param => fstring
#             if path_params:
#                 new_path = build_fstring_path(ep.path, path_params)
#             else:
#                 new_path = f'"{ep.path}"'

#             if ep.no_body:
#                 # body = {}
#                 lines.append(
#                     f"        return self.request({new_path}, body={{}}, auth=_auth)"
#                 )
#             else:
#                 if body_list:
#                     body_str = ", ".join(body_list)
#                     lines.append(
#                         f"        return self.request({new_path}, body=cleanup_dict({{ {body_str} }}), auth=_auth)"
#                     )
#                 else:
#                     lines.append(
#                         f"        return self.request({new_path}, body={{}}, auth=_auth)"
#                     )

#             lines.append("")
#         lines.append("")

#     # import SuperNevaTypes
#     excluded = {"str", "int", "bool", "date", "Any", "None", ""}
#     unique_imports = sorted(x for x in import_types if x not in excluded)
#     # remove duplicates
#     unique_imports = list(dict.fromkeys(unique_imports))
#     if unique_imports:
#         block = (
#             "from SuperNeva.Types import (\n    "
#             + ",\n    ".join(unique_imports)
#             + "\n)\n"
#         )
#         lines.insert(0, block)

#     return "\n".join(lines)


# def generate_pyi(schema: Dict[str, Any]) -> str:
#     """
#     1) endpointMapping.json'u ağaç (Node) olarak parse eder.
#     2) BFS ile Node'lardan Python sınıfları oluşturur.
#     3) ignoreArgs, body gibi özel parametreleri destekler:
#        - ignoreArgs => GraphQL arg'ları method imzasından & body'den çıkar
#        - body=false => body={} (boş)
#        - pathParam => :xyz => f"/.../{xyz}"
#        - fallback_args_if_not_found => eğer GraphQL'de yoksa ve method "list" ise,
#          _id, limit, skip, sort, filters gibi parametreleri 'Optional["str"]' ile ekler.
#     4) map_graphql_to_python(...) -> eğer tip tanınmıyorsa => "str"
#     """
#     header = [
#         "from typing import Optional, Any, List, Dict",
#         "from SuperNeva.SNRequest import SNRequest, Auth",
#         "",
#         "def cleanup_dict(d: Dict[str, Any]) -> Dict[str, Any]:",
#         "   return {k: v for k, v in d.items() if v is not None}",
#     ]
#     endpoint_mapping = load_schema(ENDPOINT_MAPPING_FILE)
#     roots = build_tree_from_mapping(endpoint_mapping)

#     schema_types = schema.get("data", {}).get("__schema", {}).get("types", [])
#     body = generate_code(roots, schema_types)
#     return "\n".join(header) + "\n" + body


# def save_pyi_file(content: str, file_path: str) -> None:
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(content)


# if __name__ == "__main__":
#     schema_data = load_schema(SCHEMA_FILE)
#     pyi_content = generate_pyi(schema_data)
#     save_pyi_file(pyi_content, OUTPUT_FILE)
#     print(f"Type hints generated in {OUTPUT_FILE}")


# NEW CODE #######################

import json
import os
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCHEMA_FILE = os.path.join(BASE_DIR, "graphql.schema.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "SuperNeva/SuperNevaAPI.py")
ENDPOINT_MAPPING_FILE = os.path.join(BASE_DIR, "endpoints.json")

print(OUTPUT_FILE)
print(SCHEMA_FILE)


def load_schema(file_path: str) -> Dict[str, Any]:
    """Belirtilen dosyadan JSON şemasını yükler."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def cleanup_null_dict_values(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


def map_graphql_to_python(type_name: str) -> str:
    """
    GraphQL scalar tiplerini Python tiplerine dönüştürür.
    Eğer tip ismi tanınmıyorsa (ör. "promptId", "skip") -> "str" olarak dön.
    """
    # Tanınan scalars
    mappings = {
        "Int": "int",
        "Float": "float",
        "String": "str",
        "Boolean": "bool",
        "ID": "str",
        "Date": "date",
        "JSON": "Any",
    }
    return mappings.get(type_name, type_name or "str")  # default fallback => "str"


# ------------------- DATA STRUCTURES -------------------
class EndpointDef:
    """
    Bir endpoint fonksiyonunu temsil eder.
    Ek Özellikler:
      ignore_args (List[str]): Bu parametreler GraphQL arg'lardan ve body'den atılacak.
      no_body (bool): true ise, request'e body={} gönderilir (body parametresi "false" ise).
    """

    def __init__(
        self,
        name: str,
        method: str,
        path: str,
        gql_type: str,
        ignore_args: List[str],
        no_body: bool,
    ):
        self.name = name
        self.method = method
        self.path = path
        self.gql_type = gql_type
        self.ignore_args = ignore_args
        self.no_body = no_body  # True => body={}


class Node:
    """
    Her Node, tek bir sınıfı temsil eder.
    - path_tokens: ['Accounts','me','collections'] => class_name: "AccountsMeCollections"
    - method_name: Ebeveynin ctor'unda self.<method_name> = <class_name>(...) => "collections"
    - endpoints: Bu node'a ait fonksiyon tanımları (EndpointDef listesi)
    - children: Alt Node listesi
    """

    def __init__(self, path_tokens: List[str], method_name: str):
        self.path_tokens = path_tokens
        self.method_name = method_name
        self.class_name = "".join(token.capitalize() for token in path_tokens if token)
        self.endpoints: List[EndpointDef] = []
        self.children: List["Node"] = []


# ------------------- PARSE MAPPING -------------------
def build_tree_from_mapping(mapping: Dict[str, Any]) -> List[Node]:
    """endpointMapping'in top-level key'leri için kök Node'lar oluştur."""
    roots: List[Node] = []
    for top_key, items in mapping.items():
        root_node = Node([top_key], method_name=top_key.lower())
        parse_items(items, root_node)
        roots.append(root_node)
    return roots


def parse_items(items: Any, parent: Node):
    """items genellikle list olur. Her elemanı parse_item'e gönderir."""
    if isinstance(items, list):
        for it in items:  # type: ignore
            parse_item(it, parent)  # type: ignore
    elif isinstance(items, dict):
        parse_item(items, parent)  # type: ignore
    else:
        pass


def parse_item(item: Dict[str, Any], parent: Node):
    """
    Bir item inceler:
      - "method","name","path","type" => endpoint
      - "ignoreArgs", "body" => ek parametreler
      - "endpoints" => alt resource
    """
    has_endpoint_fields = all(k in item for k in ("method", "name", "path", "type"))
    endpoints_data = item.get("endpoints")
    method_val = item.get("method") or ""
    name_val = item.get("name") or ""
    path_val = item.get("path") or ""
    gql_type = item.get("type") or ""

    # ignoreArgs ve body
    ignore_args: List[str] = item.get("ignoreArgs", [])
    body_param = item.get("body", True)  # default True => normal body
    no_body = body_param is False

    # "pass-through" check:
    if not method_val and not name_val and endpoints_data:
        # sadece alt endpoints var => parent'a ekle
        parse_items(endpoints_data, parent)
        return

    # alt "endpoints" var => child node
    if endpoints_data and isinstance(endpoints_data, list):
        seg = method_val or name_val or "unknown"
        child_node = Node(parent.path_tokens + [seg], method_name=seg)

        # eğer bu item aynı zamanda endpoint parametrelerine de sahipse => ekle
        if has_endpoint_fields:
            ep = EndpointDef(
                name_val, method_val, path_val, gql_type, ignore_args, no_body
            )
            child_node.endpoints.append(ep)

        parse_items(endpoints_data, child_node)
        parent.children.append(child_node)
    else:
        # leaf endpoint => direkt parent'a ekle
        if has_endpoint_fields:
            ep = EndpointDef(
                name_val, method_val, path_val, gql_type, ignore_args, no_body
            )
            parent.endpoints.append(ep)


# ------------------- GRAPHQL HELPER -------------------
def get_graphql_field(
    schema_types: List[Dict[str, Any]], gql_type: str, gql_name: str
) -> Dict[str, Any]:
    """
    GraphQL tip listesi içinde gql_type ("Query","Mutation" vs.), fields içinde gql_name'i döndür.
    Yoksa {}
    """
    tdef = next((t for t in schema_types if t["name"] == gql_type), None)
    if not tdef:
        return {}
    fields = tdef.get("fields", [])
    return next((f for f in fields if f["name"] == gql_name), {})  # type: ignore


def resolve_arg_import_type(argdef: Dict[str, Any]) -> Optional[str]:
    """
    Arg definition'ının import tipini döndürür.
    """
    type = argdef.get("type", {})
    if type.get("kind") == "NON_NULL":
        type = type.get("ofType", {})
        if type.get("kind") == "LIST":
            type = type.get("ofType", {})
            if type.get("kind") == "NON_NULL":
                type = type.get("ofType", {})
    if type.get("kind") == "LIST":
        type = type.get("ofType", {})
        if type.get("kind") == "NON_NULL":
            type = type.get("ofType", {})
    if type.get("kind") == "SCALAR":
        return None
    return type.get("name", "Any")


def map_graphql_arg_type(arg_def: Dict[str, Any]) -> str:
    """
    Maps GraphQL type definitions to Python type hints recursively.
    Handles nested NON_NULL and LIST types.
    Returns Python type hints like: str, Optional[str], List[str], Optional[List[str]], etc.
    """

    def handle_type(type_def: Dict[str, Any], inside_list: bool = False) -> str:
        if not type_def:
            return '"Any"'

        kind = type_def.get("kind")
        name = type_def.get("name")
        of_type = type_def.get("ofType", {})

        if kind == "NON_NULL":
            inner = handle_type(of_type, inside_list)
            if inside_list:
                return inner
            if inner.startswith("Optional["):
                return inner[9:-1]
            if inner.startswith('"') and inner.endswith('"'):
                return inner[1:-1]
            return inner
        elif kind == "LIST":
            inner_type = handle_type(of_type, True)
            return f"Optional[List[{inner_type}]]"
        elif name:
            mapped_type = map_graphql_to_python(name)
            return (
                f'Optional["{mapped_type}"]' if not inside_list else f'"{mapped_type}"'
            )
        else:
            return '"Any"'

    type_def = arg_def.get("type", {})
    result = handle_type(type_def)
    return result


def extract_path_params(path_str: str) -> List[str]:
    """
    /accounts/me/states/:stateId => ["stateId"]
    /some/:a/plus/:b => ["a","b"]
    """
    parts = path_str.split("/")
    return [seg[1:] for seg in parts if seg.startswith(":") and len(seg) > 1]


def build_fstring_path(path_str: str, path_params: List[str]) -> str:
    """
    :xyz -> {xyz} + f""
    """
    new_path = path_str
    for param in path_params:
        new_path = new_path.replace(f":{param}", f"{{{param}}}")
    return f'f"{new_path}"'


# ------------------- FALLBACK ARGS (ör. list) -------------------
def fallback_args_if_not_found(method_name: str) -> List[Dict[str, Any]]:
    """
    Eğer GraphQL'de field yoksa ve method 'list' ise => ek parametreler
    """
    if method_name == "list":

        def mkarg(nm: str):
            return {"name": nm, "type": {"kind": "SCALAR", "name": "String"}}

        return [
            mkarg("_id"),
            mkarg("limit"),
            mkarg("skip"),
            mkarg("sort"),
            mkarg("filters"),
        ]
    return []


# ------------------- CODE GENERATION -------------------
def generate_code(roots: List[Node], schema_types: List[Dict[str, Any]]) -> str:
    """
    BFS sırayla: Node -> class
    Each Node => class <class_name>(SNRequest):
        def __init__(...):
            super().__init__(*args, **kwargs)
            self.<childName> = <childClass>(...)
        def <endpoint_method>(...):
            ...
    """
    from collections import deque

    lines: List[str] = []
    import_types: List[str] = []
    visited: set[str] = set()
    queue = deque(roots)

    while queue:
        node = queue.popleft()
        if node.class_name in visited:
            continue
        visited.add(node.class_name)

        for child in node.children:
            queue.append(child)

        # Sınıf başlığı
        lines.append(f"class SN{node.class_name}(SNRequest):")
        lines.append("    def __init__(self, *args: Any, **kwargs: Any) -> None:")
        lines.append("        super().__init__(*args, **kwargs)")

        # Alt node referansları
        for c in node.children:
            lines.append(
                f"        self.{c.method_name} = SN{c.class_name}(*args, **kwargs)"
            )
        lines.append("")

        # Endpoint metodları
        for ep in node.endpoints:
            # GraphQL field
            gql_field = get_graphql_field(schema_types, ep.gql_type, ep.name)
            if not gql_field:
                # fallback (örneğin method=='list')
                fallback = fallback_args_if_not_found(ep.method)
                gql_field = {"args": fallback, "type": {"name": "Any"}}

            ret_type = gql_field.get("type", {}).get("name", "Any")  # type: ignore
            if (
                ret_type
                and ret_type not in ("Any", "")
                and ret_type not in import_types
            ):
                import_types.append(ret_type)  # type: ignore

            field_args: List[Dict[str, Any]] | Any = gql_field.get("args", [])

            # Path param analizi
            path_params = extract_path_params(ep.path)
            path_params_set = set(path_params)

            arg_list: List[str] = []
            body_list: List[str] = []

            for argdef in field_args:
                arg_name = argdef["name"]  # type: ignore
                if arg_name in ep.ignore_args:
                    # Bu parametre ignoreArgs'ta => yok say
                    continue
                pytype = map_graphql_arg_type(argdef)  # type: ignore

                # Tip import vs.
                import_type = resolve_arg_import_type(argdef)
                if import_type is not None:
                    import_types.append(import_type)

                # OPSİYONEL ARGÜMANLARA =None EKLEME
                # --------------------------------------------------
                # Eğer pytype "Optional[..." ile başlıyorsa,
                # method imzasında "=None" ekleyelim:
                param_decl = f"{arg_name}: {pytype}"
                if pytype.startswith("Optional["):
                    # => ...=None
                    param_decl += "=None"

                # path param?
                if arg_name in path_params_set:
                    # method imzasına ekle, body'ye koyma
                    arg_list.append(param_decl)
                else:
                    arg_list.append(param_decl)
                    # body=true ise => body'ye ekle
                    if not ep.no_body:
                        body_list.append(f'"{arg_name}": {arg_name}')

            # method signature
            if arg_list:
                signature_args = ", ".join(arg_list) + ", _auth: Optional[Auth] = None"
            else:
                signature_args = "_auth: Optional[Auth] = None"

            lines.append(f"    def {ep.method}(self, {signature_args}) -> {ret_type}:")

            # path param => fstring
            if path_params:
                new_path = build_fstring_path(ep.path, path_params)
            else:
                new_path = f'"{ep.path}"'

            if ep.no_body:
                # body = {}
                lines.append(
                    f"        return self.request({new_path}, body={{}}, auth=_auth)"
                )
            else:
                if body_list:
                    body_str = ", ".join(body_list)
                    lines.append(
                        f"        return self.request({new_path}, body=cleanup_null_dict_values({{ {body_str} }}), auth=_auth)"
                    )
                else:
                    lines.append(
                        f"        return self.request({new_path}, body={{}}, auth=_auth)"
                    )

            lines.append("")
        lines.append("")

    # import SuperNevaTypes
    excluded = {"str", "int", "bool", "date", "Any", "None", ""}
    unique_imports = sorted(x for x in import_types if x not in excluded)
    # remove duplicates
    unique_imports = list(dict.fromkeys(unique_imports))
    if unique_imports:
        block = (
            "from SuperNeva.Types import (\n    "
            + ",\n    ".join(unique_imports)
            + "\n)\n"
        )
        lines.insert(0, block)

    return "\n".join(lines)


def generate_pyi(schema: Dict[str, Any]) -> str:
    """
    1) endpointMapping.json'u ağaç (Node) olarak parse eder.
    2) BFS ile Node'lardan Python sınıfları oluşturur.
    3) ignoreArgs, body gibi özel parametreleri destekler:
       - ignoreArgs => GraphQL arg'ları method imzasından & body'den çıkar
       - body=false => body={} (boş)
       - pathParam => :xyz => f"/.../{xyz}"
       - fallback_args_if_not_found => eğer GraphQL'de yoksa ve method "list" ise,
         _id, limit, skip, sort, filters gibi parametreleri 'Optional["str"]' ile ekler.
    4) map_graphql_to_python(...) -> eğer tip tanınmıyorsa => "str"
    5) ***Ek Güncelleme***:
       - "Optional[...]" parametrelerin method imzasında "=None" ile tanımlanması
         (örn. param: Optional["str"] => param: Optional["str"]=None)
    """
    header = [
        "from typing import Optional, Any, List, Dict",
        "from SuperNeva.SNRequest import SNRequest, Auth",
        "",
        "def cleanup_null_dict_values(d: Dict[str, Any]) -> Dict[str, Any]:",
        "   return {k: v for k, v in d.items() if v is not None}",
    ]
    endpoint_mapping = load_schema(ENDPOINT_MAPPING_FILE)
    roots = build_tree_from_mapping(endpoint_mapping)

    schema_types = schema.get("data", {}).get("__schema", {}).get("types", [])
    body = generate_code(roots, schema_types)
    return "\n".join(header) + "\n" + body


def save_pyi_file(content: str, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    schema_data = load_schema(SCHEMA_FILE)
    pyi_content = generate_pyi(schema_data)
    save_pyi_file(pyi_content, OUTPUT_FILE)
    print(f"Type hints generated in {OUTPUT_FILE}")
