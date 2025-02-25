from typing import Optional, Any, List, Dict
from SuperNeva.SNRequest import SNRequest, Auth


def cleanup_dict(d: Dict[str, Any]) -> Dict[str, Any]:
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
    TargetListSortInput,
)


class SNPrompts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, promptId: "str", _auth: Optional[Auth] = None) -> Prompt:
        return self.request(f"/prompts/{promptId}", body={}, auth=_auth)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["PromptListSortInput"]],
        filters: Optional["PromptListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> PromptList:
        return self.request(
            "/prompts",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def run(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/prompts/run", body={}, auth=_auth)


class SNTargets(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["TargetListSortInput"]],
        filters: Optional["TargetListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> TargetList:
        return self.request(
            "/targets",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def get(self, targetId: "str", _auth: Optional[Auth] = None) -> Target:
        return self.request(f"/targets/{targetId}", body={}, auth=_auth)


class SNReactions(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["ReactionListSortInput"]],
        filters: Optional["ReactionListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> ReactionList:
        return self.request(
            "/reactions",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )


class SNMetas(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, metaId: "str", _auth: Optional[Auth] = None) -> Meta:
        return self.request(f"/metas/{metaId}", body={}, auth=_auth)

    def create(self, data: List["MetaInput"], _auth: Optional[Auth] = None) -> MetaList:
        return self.request(
            "metas/create", body=cleanup_dict({"data": data}), auth=_auth
        )

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["MetaListSortInput"]],
        filters: Optional["MetaListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> MetaList:
        return self.request(
            "/metas",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )


class SNLogs(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def create(
        self, data: List["LogInput"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(
            "/logs/create", body=cleanup_dict({"data": data}), auth=_auth
        )


class SNInterests(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def create(
        self,
        data: "InterestInput",
        cleanCache: Optional["bool"],
        _auth: Optional[Auth] = None,
    ) -> Interest:
        return self.request(
            "/interests/create",
            body=cleanup_dict({"data": data, "cleanCache": cleanCache}),
            auth=_auth,
        )


class SNInfo(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(
        self,
        locale: Optional["Locale"],
        clientType: Optional["str"],
        clientVersion: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Info:
        return self.request(
            "/info",
            body=cleanup_dict(
                {
                    "locale": locale,
                    "clientType": clientType,
                    "clientVersion": clientVersion,
                }
            ),
            auth=_auth,
        )


class SNFiles(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def upload(
        self,
        data: "str",
        contentType: "str",
        filename: Optional["str"],
        path: Optional["str"],
        key: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> File:
        return self.request(
            "/files/upload",
            body=cleanup_dict(
                {
                    "data": data,
                    "contentType": contentType,
                    "filename": filename,
                    "path": path,
                    "key": key,
                }
            ),
            auth=_auth,
        )


class SNContents(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(
        self,
        contentId: Optional["str"],
        key: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Content:
        return self.request(f"/contents/{contentId}", body={}, auth=_auth)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["ContentListSortInput"]],
        filters: Optional["ContentListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> ContentList:
        return self.request(
            "/contents",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )


class SNCollections(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, collectionId: "str", _auth: Optional[Auth] = None) -> Collection:
        return self.request(f"/collections/{collectionId}", body={}, auth=_auth)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["CollectionListSortInput"]],
        filters: Optional["CollectionListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> CollectionList:
        return self.request(
            "/collections",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )


class SNAuth(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def registerTargets(self, _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request("/auth/register-targets", body={}, auth=_auth)

    def isServiceConnected(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/auth/is-service-connected", body={}, auth=_auth)

    def loginWithToken(self, token: "str", _auth: Optional[Auth] = None) -> Session:
        return self.request(
            "/auth/login-with-token", body=cleanup_dict({"token": token}), auth=_auth
        )

    def connectWithService(
        self,
        data: Optional["Any"],
        service: "ServiceInput",
        targetId: Optional["str"],
        targetKey: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Session:
        return self.request(
            "/auth/connect-with-service",
            body=cleanup_dict(
                {
                    "data": data,
                    "service": service,
                    "targetId": targetId,
                    "targetKey": targetKey,
                }
            ),
            auth=_auth,
        )

    def createAccount(
        self,
        email: "str",
        password: "str",
        profile: Optional["AccountProfileInput"],
        settings: Optional["AccountSettingsInput"],
        targetId: Optional["str"],
        targetKey: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Session:
        return self.request(
            "/auth/create-account",
            body=cleanup_dict(
                {
                    "email": email,
                    "password": password,
                    "profile": profile,
                    "settings": settings,
                    "targetId": targetId,
                    "targetKey": targetKey,
                }
            ),
            auth=_auth,
        )


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
        return self.request(
            f"/accounts/me/collections/{collectionId}", body={}, auth=_auth
        )

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["CollectionListSortInput"]],
        filters: Optional["CollectionListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> CollectionList:
        return self.request(
            "/accounts/me/collections",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def create(
        self, data: "CollectionInput", _auth: Optional[Auth] = None
    ) -> Collection:
        return self.request(
            "/accounts/me/collections/create",
            body=cleanup_dict({"data": data}),
            auth=_auth,
        )

    def delete(
        self, collectionId: "str", _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(
            f"/accounts/me/collections/delete/{collectionId}", body={}, auth=_auth
        )

    def update(
        self, collectionId: "str", data: "CollectionInput", _auth: Optional[Auth] = None
    ) -> Collection:
        return self.request(
            "/accounts/me/collections/update",
            body=cleanup_dict({"collectionId": collectionId, "data": data}),
            auth=_auth,
        )

    def removeContentFromCollection(
        self, collectionId: "str", contentId: "str", _auth: Optional[Auth] = None
    ) -> Collection:
        return self.request(
            "/accounts/me/collections/remove-content-from-collection",
            body=cleanup_dict({"collectionId": collectionId, "contentId": contentId}),
            auth=_auth,
        )

    def addContentToCollection(
        self, collectionId: "str", contentId: "str", _auth: Optional[Auth] = None
    ) -> Collection:
        return self.request(
            "/api/v1/accounts/me/collections/add-content-to-collection",
            body=cleanup_dict({"collectionId": collectionId, "contentId": contentId}),
            auth=_auth,
        )


class SNAccountsMeContents(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["ContentListSortInput"]],
        filters: Optional["ContentListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> ContentList:
        return self.request(
            "/accounts/me/contents",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def create(self, data: "ContentInput", _auth: Optional[Auth] = None) -> Content:
        return self.request(
            "/accounts/me/contents/create",
            body=cleanup_dict({"data": data}),
            auth=_auth,
        )

    def delete(self, contentId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(
            f"/accounts/me/contents/delete/{contentId}", body={}, auth=_auth
        )

    def update(
        self, contentId: "str", data: "ContentInput", _auth: Optional[Auth] = None
    ) -> Content:
        return self.request(
            "/accounts/me/contents/update",
            body=cleanup_dict({"contentId": contentId, "data": data}),
            auth=_auth,
        )

    def get(self, contentId: "str", _auth: Optional[Auth] = None) -> Content:
        return self.request(f"/accounts/me/contents/{contentId}", body={}, auth=_auth)


class SNAccountsMeDevices(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["DeviceListSortInput"]],
        filters: Optional["DeviceListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> DeviceList:
        return self.request(
            "/accounts/me/devices",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def save(self, data: "DeviceInput", _auth: Optional[Auth] = None) -> Device:
        return self.request(
            "/accounts/me/devices/save", body=cleanup_dict({"data": data}), auth=_auth
        )

    def update(
        self, deviceId: "str", data: "DeviceInput", _auth: Optional[Auth] = None
    ) -> Device:
        return self.request(
            "/accounts/me/devices/update",
            body=cleanup_dict({"deviceId": deviceId, "data": data}),
            auth=_auth,
        )

    def delete(self, deviceId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(
            f"/accounts/me/devices/delete/{deviceId}", body={}, auth=_auth
        )

    def get(self, deviceId: "str", _auth: Optional[Auth] = None) -> Device:
        return self.request(f"/accounts/me/devices/{deviceId}", body={}, auth=_auth)


class SNAccountsMeInterests(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["InterestListSortInput"]],
        filters: Optional["InterestListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> InterestList:
        return self.request(
            "/accounts/me/interests",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def get(self, interestId: "str", _auth: Optional[Auth] = None) -> Interest:
        return self.request(f"/accounts/me/interests/{interestId}", body={}, auth=_auth)

    def create(
        self,
        data: "InterestInput",
        cleanCache: Optional["bool"],
        _auth: Optional[Auth] = None,
    ) -> Interest:
        return self.request(
            "/accounts/me/interests/create",
            body=cleanup_dict({"data": data, "cleanCache": cleanCache}),
            auth=_auth,
        )

    def delete(self, interestId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(
            f"/accounts/me/interests/delete/{interestId}", body={}, auth=_auth
        )


class SNAccountsMeLocations(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["LocationListSortInput"]],
        filters: Optional["LocationListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> LocationList:
        return self.request(
            "/accounts/me/locations",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def register(self, data: "LocationInput", _auth: Optional[Auth] = None) -> Location:
        return self.request(
            "/accounts/me/locations/register",
            body=cleanup_dict({"data": data}),
            auth=_auth,
        )

    def deleteAll(
        self, deviceId: "str", _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(
            "/accounts/me/locations/delete-all",
            body=cleanup_dict({"deviceId": deviceId}),
            auth=_auth,
        )


class SNAccountsMeLogs(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["LogListSortInput"]],
        filters: Optional["LogListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> LogList:
        return self.request(
            "/accounts/me/logs",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def create(
        self, data: List["LogInput"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(
            "/accounts/me/logs/create", body=cleanup_dict({"data": data}), auth=_auth
        )


class SNAccountsMePrompts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["PromptListSortInput"]],
        filters: Optional["PromptListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> PromptList:
        return self.request(
            "/accounts/me/prompts",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def get(self, promptId: "str", _auth: Optional[Auth] = None) -> Prompt:
        return self.request(f"/accounts/me/prompts/{promptId}", body={}, auth=_auth)

    def create(self, data: "PromptInput", _auth: Optional[Auth] = None) -> Prompt:
        return self.request(
            "/accounts/me/prompts/create", body=cleanup_dict({"data": data}), auth=_auth
        )

    def update(
        self, promptId: "str", data: "PromptInput", _auth: Optional[Auth] = None
    ) -> Prompt:
        return self.request(
            "/accounts/me/prompts/update",
            body=cleanup_dict({"promptId": promptId, "data": data}),
            auth=_auth,
        )

    def delete(self, promptId: "str", _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request(
            f"/accounts/me/prompts/delete/{promptId}", body={}, auth=_auth
        )


class SNAccountsMeReactions(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def save(
        self,
        data: "ReactionInput",
        skipNotification: Optional["bool"],
        _auth: Optional[Auth] = None,
    ) -> Reaction:
        return self.request(
            "/accounts/me/reactions/save",
            body=cleanup_dict({"data": data, "skipNotification": skipNotification}),
            auth=_auth,
        )


class SNAccountsMeStates(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["int"],
        skip: Optional["int"],
        sort: Optional[List["StateListSortInput"]],
        filters: Optional["StateListFilterInput"],
        _auth: Optional[Auth] = None,
    ) -> StateList:
        return self.request(
            "/accounts/me/states",
            body=cleanup_dict(
                {
                    "_id": _id,
                    "limit": limit,
                    "skip": skip,
                    "sort": sort,
                    "filters": filters,
                }
            ),
            auth=_auth,
        )

    def get(self, stateId: Optional["str"], _auth: Optional[Auth] = None) -> State:
        return self.request(f"/accounts/me/states/{stateId}", body={}, auth=_auth)

    def save(self, data: "StateInput", _auth: Optional[Auth] = None) -> State:
        return self.request(
            "/accounts/me/states/save", body=cleanup_dict({"data": data}), auth=_auth
        )
