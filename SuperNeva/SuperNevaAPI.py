from typing import Optional, Any, List, Dict
from SuperNeva.SNRequest import SNRequest, Auth

def cleanup_null_dict_values(d: Dict[str, Any]) -> Dict[str, Any]:
   return {k: v for k, v in d.items() if v is not None}
from SuperNeva.Types import (
    Account,
    AccountProfileInput,
    AccountSettingsInput,
    Collection,
    CollectionInput,
    CollectionList,
    CollectionListFilterInput,
    CollectionListSortInput,
    Content,
    ContentInput,
    ContentList,
    ContentListFilterInput,
    ContentListSortInput,
    Device,
    DeviceInput,
    DeviceList,
    DeviceListFilterInput,
    DeviceListSortInput,
    File,
    Info,
    Interest,
    InterestInput,
    InterestList,
    InterestListFilterInput,
    InterestListSortInput,
    Locale,
    Location,
    LocationInput,
    LocationList,
    LocationListFilterInput,
    LocationListSortInput,
    LogInput,
    LogList,
    LogListFilterInput,
    LogListSortInput,
    Meta,
    MetaInput,
    MetaList,
    MetaListFilterInput,
    MetaListSortInput,
    Prompt,
    PromptInput,
    PromptList,
    PromptListFilterInput,
    PromptListSortInput,
    Reaction,
    ReactionInput,
    ReactionList,
    ReactionListFilterInput,
    ReactionListSortInput,
    ServiceInput,
    Session,
    SimpleResponse,
    State,
    StateInput,
    StateList,
    StateListFilterInput,
    StateListSortInput,
    Target,
    TargetList,
    TargetListFilterInput,
    TargetListSortInput
)

class SNPrompts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, promptId: "str", _auth: Optional[Auth] = None) -> Prompt:
        return self.request(f"/prompts/{promptId}", body={}, auth=_auth)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["PromptListSortInput"]]=None, filters: Optional["PromptListFilterInput"]=None, _auth: Optional[Auth] = None) -> PromptList:
        return self.request("/prompts", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def run(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/prompts/run", body={}, auth=_auth)


class SNTargets(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["TargetListSortInput"]]=None, filters: Optional["TargetListFilterInput"]=None, _auth: Optional[Auth] = None) -> TargetList:
        return self.request("/targets", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def get(self, targetId: "str", _auth: Optional[Auth] = None) -> Target:
        return self.request(f"/targets/{targetId}", body={}, auth=_auth)


class SNReactions(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["ReactionListSortInput"]]=None, filters: Optional["ReactionListFilterInput"]=None, _auth: Optional[Auth] = None) -> ReactionList:
        return self.request("/reactions", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)


class SNMetas(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, metaId: "str", _auth: Optional[Auth] = None) -> Meta:
        return self.request(f"/metas/{metaId}", body={}, auth=_auth)

    def create(self, data: List["MetaInput"], _auth: Optional[Auth] = None) -> MetaList:
        return self.request("/metas/create", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["MetaListSortInput"]]=None, filters: Optional["MetaListFilterInput"]=None, _auth: Optional[Auth] = None) -> MetaList:
        return self.request("/metas", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)


class SNLogs(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def create(self, data: List["LogInput"], _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request("/logs/create", body=cleanup_null_dict_values({ "data": data }), auth=_auth)


class SNInterests(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def create(self, data: "InterestInput", cleanCache: Optional["bool"]=None, _auth: Optional[Auth] = None) -> Interest:
        return self.request("/interests/create", body=cleanup_null_dict_values({ "data": data, "cleanCache": cleanCache }), auth=_auth)


class SNInfo(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, locale: Optional["Locale"]=None, clientType: Optional["str"]=None, clientVersion: Optional["str"]=None, _auth: Optional[Auth] = None) -> Info:
        return self.request("/info", body=cleanup_null_dict_values({ "locale": locale, "clientType": clientType, "clientVersion": clientVersion }), auth=_auth)


class SNFiles(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def upload(self, data: "str", contentType: "str", filename: Optional["str"]=None, path: Optional["str"]=None, key: Optional["str"]=None, _auth: Optional[Auth] = None) -> File:
        return self.request("/files/upload", body=cleanup_null_dict_values({ "data": data, "contentType": contentType, "filename": filename, "path": path, "key": key }), auth=_auth)


class SNContents(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, contentId: Optional["str"]=None, key: Optional["str"]=None, _auth: Optional[Auth] = None) -> Content:
        return self.request(f"/contents/{contentId}", body={}, auth=_auth)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["ContentListSortInput"]]=None, filters: Optional["ContentListFilterInput"]=None, _auth: Optional[Auth] = None) -> ContentList:
        return self.request("/contents", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)


class SNCollections(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, collectionId: "str", _auth: Optional[Auth] = None) -> Collection:
        return self.request(f"/collections/{collectionId}", body={}, auth=_auth)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["CollectionListSortInput"]]=None, filters: Optional["CollectionListFilterInput"]=None, _auth: Optional[Auth] = None) -> CollectionList:
        return self.request("/collections", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)


class SNAuth(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def registerTargets(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/auth/register-targets", body={}, auth=_auth)

    def isServiceConnected(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/auth/is-service-connected", body={}, auth=_auth)

    def loginWithToken(self, token: "str", _auth: Optional[Auth] = None) -> Session:
        return self.request("/auth/login-with-token", body=cleanup_null_dict_values({ "token": token }), auth=_auth)

    def connectWithService(self, service: "ServiceInput", data: Optional["Any"]=None, _auth: Optional[Auth] = None) -> Session:
        return self.request("/auth/connect-with-service", body=cleanup_null_dict_values({ "service": service, "data": data }), auth=_auth)

    def createAccount(self, email: "str", password: "str", profile: Optional["AccountProfileInput"]=None, settings: Optional["AccountSettingsInput"]=None, _auth: Optional[Auth] = None) -> Session:
        return self.request("/auth/create-account", body=cleanup_null_dict_values({ "email": email, "password": password, "profile": profile, "settings": settings }), auth=_auth)


class SNAccounts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.me = SNAccountsMe(*args, **kwargs)


class SNAccountsMe(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.collections = SNAccountsMeCollections(*args, **kwargs)
        self.contents = SNAccountsMeContents(*args, **kwargs)
        self.devices = SNAccountsMeDevices(*args, **kwargs)
        self.interests = SNAccountsMeInterests(*args, **kwargs)
        self.locations = SNAccountsMeLocations(*args, **kwargs)
        self.logs = SNAccountsMeLogs(*args, **kwargs)
        self.prompts = SNAccountsMePrompts(*args, **kwargs)
        self.reactions = SNAccountsMeReactions(*args, **kwargs)
        self.states = SNAccountsMeStates(*args, **kwargs)

    def get(self, _auth: Optional[Auth] = None) -> Account:
        return self.request("/accounts/me", body={}, auth=_auth)


class SNAccountsMeCollections(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, collectionId: "str", _auth: Optional[Auth] = None) -> Collection:
        return self.request(f"/accounts/me/collections/{collectionId}", body={}, auth=_auth)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["CollectionListSortInput"]]=None, filters: Optional["CollectionListFilterInput"]=None, _auth: Optional[Auth] = None) -> CollectionList:
        return self.request("/accounts/me/collections", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def create(self, data: "CollectionInput", _auth: Optional[Auth] = None) -> Collection:
        return self.request("/accounts/me/collections/create", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

    def delete(self, collectionId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(f"/accounts/me/collections/delete/{collectionId}", body={}, auth=_auth)

    def update(self, collectionId: "str", data: "CollectionInput", _auth: Optional[Auth] = None) -> Collection:
        return self.request("/accounts/me/collections/update", body=cleanup_null_dict_values({ "collectionId": collectionId, "data": data }), auth=_auth)

    def removeContentFromCollection(self, collectionId: "str", contentId: "str", _auth: Optional[Auth] = None) -> Collection:
        return self.request("/accounts/me/collections/remove-content-from-collection", body=cleanup_null_dict_values({ "collectionId": collectionId, "contentId": contentId }), auth=_auth)

    def addContentToCollection(self, collectionId: "str", contentId: "str", _auth: Optional[Auth] = None) -> Collection:
        return self.request("/api/v1/accounts/me/collections/add-content-to-collection", body=cleanup_null_dict_values({ "collectionId": collectionId, "contentId": contentId }), auth=_auth)


class SNAccountsMeContents(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["ContentListSortInput"]]=None, filters: Optional["ContentListFilterInput"]=None, _auth: Optional[Auth] = None) -> ContentList:
        return self.request("/accounts/me/contents", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def create(self, data: "ContentInput", _auth: Optional[Auth] = None) -> Content:
        return self.request("/accounts/me/contents/create", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

    def delete(self, contentId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(f"/accounts/me/contents/delete/{contentId}", body={}, auth=_auth)

    def update(self, contentId: "str", data: "ContentInput", _auth: Optional[Auth] = None) -> Content:
        return self.request("/accounts/me/contents/update", body=cleanup_null_dict_values({ "contentId": contentId, "data": data }), auth=_auth)

    def get(self, contentId: "str", _auth: Optional[Auth] = None) -> Content:
        return self.request(f"/accounts/me/contents/{contentId}", body={}, auth=_auth)


class SNAccountsMeDevices(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["DeviceListSortInput"]]=None, filters: Optional["DeviceListFilterInput"]=None, _auth: Optional[Auth] = None) -> DeviceList:
        return self.request("/accounts/me/devices", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def save(self, data: "DeviceInput", _auth: Optional[Auth] = None) -> Device:
        return self.request("/accounts/me/devices/save", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

    def update(self, deviceId: "str", data: "DeviceInput", _auth: Optional[Auth] = None) -> Device:
        return self.request("/accounts/me/devices/update", body=cleanup_null_dict_values({ "deviceId": deviceId, "data": data }), auth=_auth)

    def delete(self, deviceId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(f"/accounts/me/devices/delete/{deviceId}", body={}, auth=_auth)

    def get(self, deviceId: "str", _auth: Optional[Auth] = None) -> Device:
        return self.request(f"/accounts/me/devices/{deviceId}", body={}, auth=_auth)


class SNAccountsMeInterests(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["InterestListSortInput"]]=None, filters: Optional["InterestListFilterInput"]=None, _auth: Optional[Auth] = None) -> InterestList:
        return self.request("/accounts/me/interests", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def get(self, interestId: "str", _auth: Optional[Auth] = None) -> Interest:
        return self.request(f"/accounts/me/interests/{interestId}", body={}, auth=_auth)

    def create(self, data: "InterestInput", cleanCache: Optional["bool"]=None, _auth: Optional[Auth] = None) -> Interest:
        return self.request("/accounts/me/interests/create", body=cleanup_null_dict_values({ "data": data, "cleanCache": cleanCache }), auth=_auth)

    def delete(self, interestId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(f"/accounts/me/interests/delete/{interestId}", body={}, auth=_auth)


class SNAccountsMeLocations(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["LocationListSortInput"]]=None, filters: Optional["LocationListFilterInput"]=None, _auth: Optional[Auth] = None) -> LocationList:
        return self.request("/accounts/me/locations", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def register(self, data: "LocationInput", _auth: Optional[Auth] = None) -> Location:
        return self.request("/accounts/me/locations/register", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

    def deleteAll(self, deviceId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request("/accounts/me/locations/delete-all", body=cleanup_null_dict_values({ "deviceId": deviceId }), auth=_auth)


class SNAccountsMeLogs(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["LogListSortInput"]]=None, filters: Optional["LogListFilterInput"]=None, _auth: Optional[Auth] = None) -> LogList:
        return self.request("/accounts/me/logs", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def create(self, data: List["LogInput"], _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request("/accounts/me/logs/create", body=cleanup_null_dict_values({ "data": data }), auth=_auth)


class SNAccountsMePrompts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["PromptListSortInput"]]=None, filters: Optional["PromptListFilterInput"]=None, _auth: Optional[Auth] = None) -> PromptList:
        return self.request("/accounts/me/prompts", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def get(self, promptId: "str", _auth: Optional[Auth] = None) -> Prompt:
        return self.request(f"/accounts/me/prompts/{promptId}", body={}, auth=_auth)

    def create(self, data: "PromptInput", _auth: Optional[Auth] = None) -> Prompt:
        return self.request("/accounts/me/prompts/create", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

    def update(self, promptId: "str", data: "PromptInput", _auth: Optional[Auth] = None) -> Prompt:
        return self.request("/accounts/me/prompts/update", body=cleanup_null_dict_values({ "promptId": promptId, "data": data }), auth=_auth)

    def delete(self, promptId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(f"/accounts/me/prompts/delete/{promptId}", body={}, auth=_auth)


class SNAccountsMeReactions(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def save(self, data: "ReactionInput", skipNotification: Optional["bool"]=None, _auth: Optional[Auth] = None) -> Reaction:
        return self.request("/accounts/me/reactions/save", body=cleanup_null_dict_values({ "data": data, "skipNotification": skipNotification }), auth=_auth)


class SNAccountsMeStates(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(self, _id: Optional["str"]=None, limit: Optional["int"]=None, skip: Optional["int"]=None, sort: Optional[List["StateListSortInput"]]=None, filters: Optional["StateListFilterInput"]=None, _auth: Optional[Auth] = None) -> StateList:
        return self.request("/accounts/me/states", body=cleanup_null_dict_values({ "_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters }), auth=_auth)

    def get(self, stateId: Optional["str"]=None, _auth: Optional[Auth] = None) -> State:
        return self.request(f"/accounts/me/states/{stateId}", body={}, auth=_auth)

    def save(self, data: "StateInput", _auth: Optional[Auth] = None) -> State:
        return self.request("/accounts/me/states/save", body=cleanup_null_dict_values({ "data": data }), auth=_auth)

