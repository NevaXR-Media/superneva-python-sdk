# import json
# import os
# from typing import Any, Dict, List, Optional

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SCHEMA_FILE = os.path.join(BASE_DIR, "graphql.schema.json")
# OUTPUT_FILE = os.path.join(BASE_DIR, "AIRunner/SuperNevaAPI.py")
# ENDPOINT_MAPPING_FILE = os.path.join(BASE_DIR, "endpoints.json")

# print(OUTPUT_FILE)
# print(SCHEMA_FILE)


# def load_schema(file_path: str) -> Dict[str, Any]:
#     """Belirtilen dosyadan JSON şemasını yükler."""
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)


# def map_graphql_to_python(type_name: str) -> str:
#     """GraphQL scalar tiplerini Python tiplerine dönüştürür."""
#     mappings = {
#         "Int": "int",
#         "Float": "float",
#         "String": "str",
#         "Boolean": "bool",
#         "ID": "str",
#         "Date": "date",
#         "JSON": "Any",
#     }
#     return mappings.get(type_name, type_name)


# # ------------------- DATA STRUCTURES -------------------
# class EndpointDef:
#     """
#     Bir endpoint fonksiyonunu temsil eder.
#     Örneğin:
#       { "name": "createCollection", "method": "create",
#         "path": "/accounts/me/collections/create", "type": "Mutation" }
#     """
#     def __init__(self, name: str, method: str, path: str, gql_type: str):
#         self.name = name      # GraphQL field name ("createCollection","publicPrompt", vs.)
#         self.method = method  # Fonksiyon adı ("get","list","create","update", vs.)
#         self.path = path      # REST path ("/accounts/me/collections/create")
#         self.gql_type = gql_type  # GraphQL kök tipi ("Query","Mutation", vs.)


# class Node:
#     """
#     Her Node, tek bir Sınıf'ı temsil eder.
#     - path_tokens: ['Accounts','me','collections']  => class_name: "AccountsMeCollections"
#     - method_name: Ebeveynin ctor'unda self.<method_name> = <class_name>(...) diye geçer ("collections")
#     - endpoints: Bu node'a ait fonksiyon tanımları
#     - children: Alt node listesi
#     """
#     def __init__(self, path_tokens: List[str], method_name: str):
#         self.path_tokens = path_tokens
#         self.method_name = method_name
#         self.class_name = "".join(token.capitalize() for token in path_tokens if token)
#         self.endpoints: List[EndpointDef] = []
#         self.children: List[Node] = []


# # ------------------- PARSE MAPPING -------------------
# def build_tree_from_mapping(mapping: Dict[str, Any]) -> List[Node]:
#     """
#     endpointMapping'in top-level key'leri için kök Node'lar oluştur.
#     Örn: "Accounts": [ ... ] => Node(["Accounts"], "accounts")
#     Sonra alt item'ları parse ederek BFS sıralamasına uygun bir ağaç döndürür.
#     """
#     roots: List[Node] = []

#     for top_key, items in mapping.items():
#         # Örn: top_key="Accounts"
#         # method_name = top_key.lower() => "accounts"
#         root_node = Node([top_key], method_name=top_key.lower())
#         # item'lar => parse
#         parse_items(items, root_node)
#         roots.append(root_node)

#     return roots


# def parse_items(items: Any, parent: Node):
#     """
#     items genellikle list olur. Her bir elemanı parse_item'e gönderir.
#     """
#     if isinstance(items, list):
#         for it in items:
#             parse_item(it, parent)
#     elif isinstance(items, dict):
#         parse_item(items, parent)
#     else:
#         # int/str vs. yok say
#         pass


# def parse_item(item: Dict[str, Any], parent: Node):
#     """
#     Bir item:
#       - eğer "endpoints" varsa alt node'lar içeren bir resource group olabilir,
#         ayrıca kendisi de bir endpoint (method+path vs. varsa) olabilir.
#       - eğer "method","name","path","type" varsa => endpoint.
#       - eğer "method" / "name" yoksa ve sadece "endpoints" içeriyorsa => "pass-through" (yeni node yaratmadan alt endpoints'i parent'a ekle).
#     """
#     endpoints_data = item.get("endpoints")
#     has_endpoint_fields = all(k in item for k in ("method","name","path","type"))

#     # 1) Pass-through check:
#     #    Eğer item "method" ve "name" yok veya bos, ama "endpoints" varsa => alt endpoints'i parent'a ekle.
#     #    (Böylece "unknown" class oluşmuyor)
#     method_val = item.get("method")
#     name_val   = item.get("name")
#     path_val   = item.get("path")

#     # Pass-through durumu: "method" yok VEYA "name" yok; path vb. de olmayabilir, sadece endpoints
#     # Örnek: { "endpoints": [...]}  => "unknown" class yaratmak istemiyoruz
#     if not method_val and not name_val and endpoints_data:
#         # alt endpoints'i doğrudan parent'a parse ettir
#         parse_items(endpoints_data, parent)
#         return

#     # 2) Node mu oluşturacağız?
#     if endpoints_data and isinstance(endpoints_data, list):
#         # Bu item hem alt node'lara sahip, hem belki kendisi de endpoint
#         seg = method_val or name_val
#         if not seg:
#             seg = "unknown"  # fallback

#         child_node = Node(parent.path_tokens + [seg], method_name=seg)

#         # eğer kendisi de endpoint => ekle
#         if has_endpoint_fields:
#             ep = EndpointDef(name_val, method_val, path_val, item["type"])
#             child_node.endpoints.append(ep)

#         # alt endpoints'i parse
#         parse_items(endpoints_data, child_node)

#         # parent'a ekle
#         parent.children.append(child_node)
#     else:
#         # 3) Leaf endpoint ise => doğrudan parent'a metod ekle
#         if has_endpoint_fields:
#             ep = EndpointDef(name_val, method_val, path_val, item["type"])
#             parent.endpoints.append(ep)
#         else:
#             # Geçersiz / eksik => yok say
#             pass


# # ------------------- GRAPHQL HELPER -------------------
# def get_graphql_field(schema_types: List[Dict[str, Any]], gql_type: str, gql_name: str) -> Dict[str, Any]:
#     """
#     GraphQL tip listesi içinde gql_type ("Query","Mutation" vs.) bul,
#     oradaki fields içinde gql_name'e denk geleni döndür. Yoksa {}.
#     """
#     tdef = next((t for t in schema_types if t["name"] == gql_type), None)
#     if not tdef:
#         return {}
#     fields = tdef.get("fields", [])
#     return next((f for f in fields if f["name"] == gql_name), {})


# def get_arg_type(arg_def: Dict[str, Any], import_list: List[str]) -> str:
#     """
#     NON_NULL, LIST, SCALAR vb. GraphQL tipini Python tipine dönüştürür.
#     """
#     kind = arg_def.get("kind","")
#     if kind == "NON_NULL":
#         oftype = arg_def.get("ofType", {})
#         if oftype.get("kind") == "LIST":
#             el = map_graphql_to_python(oftype["ofType"]["name"])
#             if el not in import_list:
#                 import_list.append(el)
#             return f'List["{el}"]'
#         else:
#             el = map_graphql_to_python(oftype.get("name","Any"))
#             if el not in import_list:
#                 import_list.append(el)
#             return f'"{el}"'
#     elif kind == "LIST":
#         innertype = arg_def.get("ofType",{}).get("ofType",{}).get("name","Any")
#         el = map_graphql_to_python(innertype)
#         if el not in import_list:
#             import_list.append(el)
#         return f'Optional[List["{el}"]]'
#     else:
#         # SCALAR / OBJECT
#         el = map_graphql_to_python(arg_def.get("name","Any"))
#         if el not in import_list:
#             import_list.append(el)
#         return f'Optional["{el}"]'


# # ------------------- CODE GENERATION -------------------
# def generate_code(roots: List[Node], schema_types: List[Dict[str, Any]]) -> str:
#     """
#     BFS sırayla: her Node için class tanımı yaz.
#     Ebeveyn => children => grandchildren => ...
#     """
#     from collections import deque

#     lines: List[str] = []
#     import_types: List[str] = []
#     visited = set()

#     # BFS kuyruğu
#     queue = deque(roots)

#     def build_method_args(field_args: List[Dict[str, Any]]) -> (str,str):
#         argstr_list = []
#         body_list   = []
#         for a in field_args:
#             arg_name = a["name"]
#             pytype   = get_arg_type(a["type"], import_types)
#             argstr_list.append(f"{arg_name}: {pytype}")
#             body_list.append(f"\"{arg_name}\": {arg_name}")
#         return (", ".join(argstr_list), ", ".join(body_list))

#     while queue:
#         node = queue.popleft()
#         if node.class_name in visited:
#             continue
#         visited.add(node.class_name)

#         # Children'ı queue'ya ekle
#         for c in node.children:
#             queue.append(c)

#         # Sınıf tanımı
#         lines.append(f"class {node.class_name}(SNRequest):")
#         lines.append("    def __init__(self, *args: Any, **kwargs: Any) -> None:")
#         lines.append("        super().__init__(*args, **kwargs)")

#         # alt düğümlere referans
#         for child in node.children:
#             lines.append(f"        self.{child.method_name} = {child.class_name}(*args, **kwargs)")
#         lines.append("")

#         # endpoint metodları
#         for ep in node.endpoints:
#             gql_field = get_graphql_field(schema_types, ep.gql_type, ep.name)
#             field_args = gql_field.get("args", [])
#             ret_type   = gql_field.get("type",{}).get("name","Any")
#             if ret_type and ret_type not in ("Any","") and ret_type not in import_types:
#                 import_types.append(ret_type)

#             argstr, bodystr = build_method_args(field_args)
#             if argstr.strip():
#                 signature_args = f"{argstr}, _auth: Optional[Auth] = None"
#             else:
#                 signature_args = "_auth: Optional[Auth] = None"

#             lines.append(f"    def {ep.method}(self, {signature_args}) -> {ret_type}:")
#             if bodystr.strip():
#                 lines.append(f'        return self.request("{ep.path}", body={{ {bodystr} }}, _auth=_auth)  # type: ignore')
#             else:
#                 lines.append(f'        return self.request("{ep.path}", body={{}}, _auth=_auth)  # type: ignore')
#             lines.append("")
#         lines.append("")

#     # import SuperNevaTypes
#     excluded = {"str","int","bool","date","Any","None",""}
#     # unique_imports = sorted(x for x in import_types if x not in excluded)
#     unique_imports = sorted(x for x in import_types if x and x not in excluded)


#     if unique_imports:
#         block = (
#             "from SuperNevaTypes import (\n    "
#             + ",\n    ".join(unique_imports)
#             + "\n)\n"
#         )
#         lines.insert(0, block)

#     return "\n".join(lines)


# def generate_pyi(schema: Dict[str, Any]) -> str:
#     """
#     1) endpointMapping.json'u ağaç yapısına çevirir (Node).
#     2) BFS ile node'ları gezerek, her Node için class oluşturur.
#        Ebeveyn önce, çocuk sonra.
#     3) Her node'un alt düğümlerine __init__'te self.<child> = <ChildClass>(...)
#        Node'un endpoints'i => Python metodları.
#     """
#     # Bazı sabit importlar
#     header = [
#         "from enum import Enum  # type: ignore",
#         "from datetime import date  # type: ignore",
#         "from typing import TypedDict, Optional, Any, List  # type: ignore",
#         "from SuperNeva import SNRequest, Auth",
#         ""
#     ]

#     endpoint_mapping = load_schema(ENDPOINT_MAPPING_FILE)
#     # Ağaç yapısını çıkar
#     roots = build_tree_from_mapping(endpoint_mapping)
#     # GraphQL tipi listesi
#     schema_types = schema.get("data", {}).get("__schema", {}).get("types", [])

#     # BFS kod üretimi
#     body = generate_code(roots, schema_types)
#     return "\n".join(header) + "\n" + body


# def save_pyi_file(content: str, file_path: str) -> None:
#     """Oluşturulan kodu belirtilen dosyaya yazar."""
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(content)


# if __name__ == "__main__":
#     schema_data = load_schema(SCHEMA_FILE)
#     generated = generate_pyi(schema_data)
#     save_pyi_file(generated, OUTPUT_FILE)
#     print(f"Type hints generated in {OUTPUT_FILE}")




import json
import os
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCHEMA_FILE = os.path.join(BASE_DIR, "graphql.schema.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "AIRunner/SuperNevaAPI.py")
ENDPOINT_MAPPING_FILE = os.path.join(BASE_DIR, "endpoints.json")

print(OUTPUT_FILE)
print(SCHEMA_FILE)


def load_schema(file_path: str) -> Dict[str, Any]:
    """Belirtilen dosyadan JSON şemasını yükler."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def map_graphql_to_python(type_name: str) -> str:
    """GraphQL scalar tiplerini Python tiplerine dönüştürür."""
    mappings = {
        "Int": "int",
        "Float": "float",
        "String": "str",
        "Boolean": "bool",
        "ID": "str",
        "Date": "date",
        "JSON": "Any",
    }
    return mappings.get(type_name, type_name)


def generate_pyi(schema: Dict[str, Any]) -> str:
    """
    GraphQL şemasını ve endpointMapping.json verilerini kullanarak
    derinlikli (nested) endpoint’leri 'flat' (tek seviyeli) sınıflara dönüştürür.

    - Her node (method veya name) bir path segment’idir.
    - Leaf (endpoints’i olmayan) item’lar o sınıfın metodlarını oluşturur.
    - endpoints alanı varsa, oradan yeni bir path türetilir ve
      yeni bir top-level class yaratılır (nested class yok).

    Not: Derinlik arttığında da bozulmadan çalışır.
    """

    output = [
        "from enum import Enum  # type: ignore",
        "from datetime import date  # type: ignore",
        "from typing import TypedDict, Optional, Any, List  # type: ignore",
        "from SuperNeva import SNRequest, Auth",
        ""
    ]
    
    # GraphQL tiplerini şemadan alıyoruz.
    types = schema.get("data", {}).get("__schema", {}).get("types", [])
    import_statements: List[str] = []
    
    EndpointMapping = load_schema(ENDPOINT_MAPPING_FILE)

    # Bu dict, oluşturulacak sınıfları ve metodlarını tutar.
    # class_registry[class_name] = [ {func_name, path, args, return_type, body_params}, ... ]
    class_registry: Dict[str, List[Dict[str, Any]]] = {}

    # ----------------------------------------------------------------
    #   YARDIMCI FONKSİYONLAR
    # ----------------------------------------------------------------

    def pythonize_path(path_tokens: List[str]) -> str:

        return "".join(seg[0].upper() + seg[1:] for seg in path_tokens if seg)

    def get_field_info(gql_type: str, gql_field_name: str) -> Dict[str, Any]:

        tdef = next((t for t in types if t["name"] == gql_type), None)
        if not tdef:
            return {}
        fields = tdef.get("fields", [])
        return next((f for f in fields if f["name"] == gql_field_name), {})

    def extract_args_and_return(field_info: Dict[str, Any]) -> (List[Dict[str, Any]], str): # type: ignore
        """
        field_info içinden arg listesi ve dönüş tipini al.
        """
        if not field_info:
            return [], "Any"  # type: ignore
        field_args = field_info.get("args", [])
        field_type = field_info.get("type", {})
        ret_type = field_type.get("name", "Any")
        return field_args, ret_type

    def parse_endpoint_item(path_tokens: List[str], item: Dict[str, Any]) -> None:
        """
        Tek bir endpoint item'ını işleyip, class_registry'ye metod olarak ekler.
        item içerisinde "method","name","path","type" varsa -> bu bir leaf endpoint.
        """
        gql_type = item.get("type", "")   # "Query", "Mutation", vb.
        gql_field = item.get("name", "")  # "publicPrompt", "createAccount", vb.

        # GraphQL'de parametre bilgisi arayalım
        field_info = get_field_info(gql_type, gql_field)
        field_args, return_type = extract_args_and_return(field_info)

        if return_type not in ("Any", "") and return_type not in import_statements:
            import_statements.append(return_type)

        # Argüman tiplerini parse edelim
        args_str, args_keys = build_method_args(field_args)  # type: ignore

        # Sınıf adı
        class_name = pythonize_path(path_tokens)

        # Fonksiyon adı (kullanıcı isterse method alanından, isterse name alanından alabilir)
        # Genelde "method" alanı: "list", "get", "create", "update" vs.  
        # "name" alanı: "createAccount", "publicPromptRun" vb.
        # Hangisini fonksiyon ismi yapacağınız size bağlı. Örn. 'method' kullanıyoruz.
        func_name = item["method"]

        # Body
        req_path = item["path"]
        if args_keys.strip():
            req_body = "{" + args_keys + "}"
        else:
            req_body = "{}"

        # Sınıf kaydını oluştur
        if class_name not in class_registry:
            class_registry[class_name] = []
        class_registry[class_name].append({
            "func_name": func_name,
            "return_type": return_type,
            "args_str": args_str,
            "path": req_path,
            "req_body": req_body
        })

    def build_method_args(field_args: List[Dict[str, Any]]) -> (str, str):  # type: ignore

        arg_pairs = []
        arg_body_pairs = []
        for arg in field_args:
            arg_name = arg["name"]
            py_type = map_graphql_arg_type(arg["type"], import_statements)
            arg_pairs.append(f"{arg_name}: {py_type}")
            arg_body_pairs.append(f"\"{arg_name}\": {arg_name}")
        args_str = ", ".join(arg_pairs)
        body_str = ", ".join(arg_body_pairs)
        return args_str, body_str

    def map_graphql_arg_type(type_def: Dict[str, Any], imports: List[str]) -> str:
        """
        NON_NULL, LIST, SCALAR vb. GraphQL tipini Python tipine dönüştürür.
        """
        kind = type_def.get("kind", "")
        if kind == "NON_NULL":
            of_type = type_def.get("ofType", {})
            if of_type.get("kind") == "LIST":
                el_type = map_graphql_to_python(of_type["ofType"]["name"])
                if el_type not in imports:
                    imports.append(el_type)
                return f'List["{el_type}"]'
            else:
                el_type = map_graphql_to_python(of_type.get("name", "Any"))
                if el_type not in imports:
                    imports.append(el_type)
                return f'"{el_type}"'
        elif kind == "LIST":
            # Optional list
            of_type = type_def.get("ofType", {})
            inner_name = of_type.get("ofType", {}).get("name", "Any")
            el_type = map_graphql_to_python(inner_name)
            if el_type not in imports:
                imports.append(el_type)
            return f'Optional[List["{el_type}"]]'
        else:
            # SCALAR veya OBJECT
            el_type = map_graphql_to_python(type_def.get("name", "Any"))
            if el_type not in imports:
                imports.append(el_type)
            return f'Optional["{el_type}"]'

    # ----------------------------------------------------------------
    #   DFS FONKSİYONU - DERİNLİĞİ GEZ
    # ----------------------------------------------------------------

    def dfs(path_tokens: List[str], node: Any) -> None:

        if isinstance(node, dict):
            has_endpoints = "endpoints" in node and isinstance(node["endpoints"], list)
            has_method_and_path = all(k in node for k in ("method", "path", "type", "name"))

            if has_endpoints:
                # Bu node hem bir resource (yeni path segment) hem de alt endpoint’lere sahip olabilir.
                current_method = node.get("method", "")  # path segment
                new_path = path_tokens
                if current_method:
                    new_path = path_tokens + [current_method]

                # Node'un kendisi de endpoint tanımlıyorsa => leaf method olarak ekle
                if has_method_and_path:
                    # Bu node aynı zamanda bir leaf endpoint (mesela "method": "collections" ama kendisi de path’e sahip)
                    # Bunu current sınıfa metod olarak ekle
                    parse_endpoint_item(new_path, node)

                # Şimdi alt endpoints'i gezelim
                for child in node["endpoints"]:
                    dfs(new_path, child)

            else:
                # endpoints yok => bu bir leaf endpoint
                if has_method_and_path:
                    parse_endpoint_item(path_tokens, node)

        elif isinstance(node, list):
            for child in node:
                dfs(path_tokens, child)
        else:
            # int/string vs. atla
            pass

    # ----------------------------------------------------------------
    #  1) TÜM TOP-LEVEL KEY'LERİ (Prompts, Auth, Accounts vb.) DOLAŞ
    # ----------------------------------------------------------------

    for top_key, value in EndpointMapping.items():
        # top_key = "Prompts", "Accounts", ...
        # value -> list
        dfs([top_key], value)

    # ----------------------------------------------------------------
    #  2) Elde ettiğimiz class_registry içindeki veriyi kod olarak yaz
    # ----------------------------------------------------------------

    output.append("")  # Boş satır

    for cls_name, methods in class_registry.items():
        output.append(f"class {cls_name}(SNRequest):")
        # init
        output.append("    def __init__(self, *args: Any, **kwargs: Any) -> None:")
        output.append("        super().__init__(*args, **kwargs)")
        output.append("")

        # Metodları ekleyelim
        for m in methods:
            func_name = m["func_name"]
            ret_type = m["return_type"] if m["return_type"] else "Any"
            args_str = m["args_str"]
            req_path = m["path"]
            req_body = m["req_body"]

            # _auth ekle
            if args_str:
                full_args = f"{args_str}, _auth: Optional[Auth] = None"
            else:
                full_args = "_auth: Optional[Auth] = None"

            output.append(f"    def {func_name}(self, {full_args}) -> {ret_type}:")
            output.append(f"        return self.request(\"{req_path}\", body={req_body}, _auth=_auth)  # type: ignore")
            output.append("")

        output.append("")

    # ----------------------------------------------------------------
    #  3) SuperNevaTypes importlarını ekle
    # ----------------------------------------------------------------

    excluded = {"str", "int", "bool", "date", "Any", "None", ""}
    unique_imports = sorted({imp for imp in import_statements if imp and imp not in excluded})
    if unique_imports:
        multiline_import = (
            "from SuperNevaTypes import (\n    " + ",\n    ".join(unique_imports) + "\n)"
        )
        output.insert(4, multiline_import)

    # Sonuç
    return "\n".join(output)


def save_pyi_file(content: str, file_path: str) -> None:
    """Oluşturulan kodu belirtilen dosyaya yazar."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    schema = load_schema(SCHEMA_FILE)
    pyi_content = generate_pyi(schema)
    save_pyi_file(pyi_content, OUTPUT_FILE)
    print(f"Type hints generated in {OUTPUT_FILE}")
