from enum import Enum  # type: ignore
from datetime import date  # type: ignore
from typing import TypedDict, Optional, Any, List  # type: ignore
from SuperNeva import SNRequest, Auth

from SuperNevaTypes import (
    Account,
    Collection,
    CollectionList,
    Content,
    ContentList,
    Device,
    DeviceList,
    File,
    Info,
    Interest,
    InterestList,
    Location,
    LocationList,
    LogList,
    Meta,
    MetaList,
    Prompt,
    PromptList,
    Reaction,
    ReactionList,
    Session,
    SimpleResponse,
    State,
    StateList,
    Target,
    TargetList,
)


class Prompts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, promptId: Optional["str"], _auth: Optional[Auth] = None) -> Prompt:
        return self.request(f"/prompts/{promptId}", body={}, _auth=_auth)  # type: ignore

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> PromptList:
        return self.request("/prompts", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def run(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/prompts/run", body={}, _auth=_auth)  # type: ignore


class Targets(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> TargetList:
        return self.request("/targets", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def get(self, targetId: Optional["str"], _auth: Optional[Auth] = None) -> Target:
        return self.request(f"/targets/{targetId}", body={}, _auth=_auth)  # type: ignore


class Reactions(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> ReactionList:
        return self.request("/reactions", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore


class Metas(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(self, metaId: Optional["str"], _auth: Optional[Auth] = None) -> Meta:
        return self.request(f"/metas/{metaId}", body={}, _auth=_auth)  # type: ignore

    def create(self, data: Optional["str"], _auth: Optional[Auth] = None) -> MetaList:
        return self.request("metas/create", body={"data": data}, _auth=_auth)  # type: ignore

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> MetaList:
        return self.request("/metas", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore


class Logs(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def create(
        self, data: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request("/logs/create", body={"data": data}, _auth=_auth)  # type: ignore


class Interests(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def create(
        self,
        data: Optional["str"],
        cleanCache: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Interest:
        return self.request("/interests/create", body={"data": data, "cleanCache": cleanCache}, _auth=_auth)  # type: ignore


class Info(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(
        self,
        locale: Optional["str"],
        clientType: Optional["str"],
        clientVersion: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Info:
        return self.request("/info", body={"locale": locale, "clientType": clientType, "clientVersion": clientVersion}, _auth=_auth)  # type: ignore


class Files(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def upload(
        self,
        data: Optional["str"],
        contentType: Optional["str"],
        filename: Optional["str"],
        path: Optional["str"],
        key: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> File:
        return self.request("/files/upload", body={"data": data, "contentType": contentType, "filename": filename, "path": path, "key": key}, _auth=_auth)  # type: ignore


class Contents(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(
        self,
        contentId: Optional["str"],
        key: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Content:
        return self.request(f"/contents/{contentId}", body={}, _auth=_auth)  # type: ignore

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> ContentList:
        return self.request("/contents", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore


class Collections(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(
        self, collectionId: Optional["str"], _auth: Optional[Auth] = None
    ) -> Collection:
        return self.request(f"/collections/{collectionId}", body={}, _auth=_auth)  # type: ignore

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> CollectionList:
        return self.request("/collections", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore


class Auth(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def registerTargets(self, _auth: Optional[Auth] = None) -> SimpleResponse:
        return self.request("/auth/register-targets", body={}, _auth=_auth)  # type: ignore

    def isServiceConnected(self, _auth: Optional[Auth] = None) -> Any:
        return self.request("/auth/is-service-connected", body={}, _auth=_auth)  # type: ignore

    def loginWithToken(
        self, token: Optional["str"], _auth: Optional[Auth] = None
    ) -> Session:
        return self.request("/auth/login-with-token", body={"token": token}, _auth=_auth)  # type: ignore

    def connectWithService(
        self,
        data: Optional["str"],
        service: Optional["str"],
        targetId: Optional["str"],
        targetKey: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Session:
        return self.request("/auth/connect-with-service", body={"data": data, "service": service, "targetId": targetId, "targetKey": targetKey}, _auth=_auth)  # type: ignore

    def createAccount(
        self,
        email: Optional["str"],
        password: Optional["str"],
        profile: Optional["str"],
        settings: Optional["str"],
        targetId: Optional["str"],
        targetKey: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Session:
        return self.request("/auth/create-account", body={"email": email, "password": password, "profile": profile, "settings": settings, "targetId": targetId, "targetKey": targetKey}, _auth=_auth)  # type: ignore


class Accounts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.me = AccountsMe(*args, **kwargs)


class AccountsMe(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.collections = AccountsMeCollections(*args, **kwargs)
        self.contents = AccountsMeContents(*args, **kwargs)
        self.devices = AccountsMeDevices(*args, **kwargs)
        self.interests = AccountsMeInterests(*args, **kwargs)
        self.locations = AccountsMeLocations(*args, **kwargs)
        self.logs = AccountsMeLogs(*args, **kwargs)
        self.prompts = AccountsMePrompts(*args, **kwargs)
        self.reactions = AccountsMeReactions(*args, **kwargs)
        self.states = AccountsMeStates(*args, **kwargs)

    def get(self, _auth: Optional[Auth] = None) -> Account:
        return self.request("/accounts/me", body={}, _auth=_auth)  # type: ignore


class AccountsMeCollections(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get(
        self, collectionId: Optional["str"], _auth: Optional[Auth] = None
    ) -> Collection:
        return self.request(f"/accounts/me/collections/{collectionId}", body={}, _auth=_auth)  # type: ignore

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> CollectionList:
        return self.request("/accounts/me/collections", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def create(self, data: Optional["str"], _auth: Optional[Auth] = None) -> Collection:
        return self.request("/accounts/me/collections/create", body={"data": data}, _auth=_auth)  # type: ignore

    def delete(
        self, collectionId: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(f"/accounts/me/collections/delete/{collectionId}", body={}, _auth=_auth)  # type: ignore

    def update(
        self,
        collectionId: Optional["str"],
        data: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Collection:
        return self.request("/accounts/me/collections/update", body={"collectionId": collectionId, "data": data}, _auth=_auth)  # type: ignore

    def removeContentFromCollection(
        self,
        collectionId: Optional["str"],
        contentId: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Collection:
        return self.request("/accounts/me/collections/remove-content-from-collection", body={"collectionId": collectionId, "contentId": contentId}, _auth=_auth)  # type: ignore

    def addContentToCollection(
        self,
        collectionId: Optional["str"],
        contentId: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Collection:
        return self.request("/api/v1/accounts/me/collections/add-content-to-collection", body={"collectionId": collectionId, "contentId": contentId}, _auth=_auth)  # type: ignore


class AccountsMeContents(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> ContentList:
        return self.request("/accounts/me/contents", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def create(self, data: Optional["str"], _auth: Optional[Auth] = None) -> Content:
        return self.request("/accounts/me/contents/create", body={"data": data}, _auth=_auth)  # type: ignore

    def delete(
        self, contentId: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(f"/accounts/me/contents/delete/{contentId}", body={}, _auth=_auth)  # type: ignore

    def update(
        self,
        contentId: Optional["str"],
        data: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Content:
        return self.request("/accounts/me/contents/update", body={"contentId": contentId, "data": data}, _auth=_auth)  # type: ignore

    def get(self, contentId: Optional["str"], _auth: Optional[Auth] = None) -> Content:
        return self.request(f"/accounts/me/contents/{contentId}", body={}, _auth=_auth)  # type: ignore


class AccountsMeDevices(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> DeviceList:
        return self.request("/accounts/me/devices", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def save(self, data: Optional["str"], _auth: Optional[Auth] = None) -> Device:
        return self.request("/accounts/me/devices/save", body={"data": data}, _auth=_auth)  # type: ignore

    def update(
        self,
        deviceId: Optional["str"],
        data: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Device:
        return self.request("/accounts/me/devices/update", body={"deviceId": deviceId, "data": data}, _auth=_auth)  # type: ignore

    def delete(
        self, deviceId: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(f"/accounts/me/devices/delete/{deviceId}", body={}, _auth=_auth)  # type: ignore

    def get(self, deviceId: Optional["str"], _auth: Optional[Auth] = None) -> Device:
        return self.request(f"/accounts/me/devices/{deviceId}", body={}, _auth=_auth)  # type: ignore


class AccountsMeInterests(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> InterestList:
        return self.request("/accounts/me/interests", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def get(
        self, interestId: Optional["str"], _auth: Optional[Auth] = None
    ) -> Interest:
        return self.request(f"/accounts/me/interests/{interestId}", body={}, _auth=_auth)  # type: ignore

    def create(
        self,
        data: Optional["str"],
        cleanCache: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Interest:
        return self.request("/accounts/me/interests/create", body={"data": data, "cleanCache": cleanCache}, _auth=_auth)  # type: ignore

    def delete(
        self, interestId: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(f"/accounts/me/interests/delete/{interestId}", body={}, _auth=_auth)  # type: ignore


class AccountsMeLocations(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> LocationList:
        return self.request("/accounts/me/locations", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def register(self, data: Optional["str"], _auth: Optional[Auth] = None) -> Location:
        return self.request("/accounts/me/locations/register", body={"data": data}, _auth=_auth)  # type: ignore

    def deleteAll(
        self, deviceId: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request("/accounts/me/locations/delete-all", body={"deviceId": deviceId}, _auth=_auth)  # type: ignore


class AccountsMeLogs(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> LogList:
        return self.request("/accounts/me/logs", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def create(
        self, data: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request("/accounts/me/logs/create", body={"data": data}, _auth=_auth)  # type: ignore


class AccountsMePrompts(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> PromptList:
        return self.request("/accounts/me/prompts", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def get(self, promptId: Optional["str"], _auth: Optional[Auth] = None) -> Prompt:
        return self.request(f"/accounts/me/prompts/{promptId}", body={}, _auth=_auth)  # type: ignore

    def create(self, data: Optional["str"], _auth: Optional[Auth] = None) -> Prompt:
        return self.request("/accounts/me/prompts/create", body={"data": data}, _auth=_auth)  # type: ignore

    def update(
        self,
        promptId: Optional["str"],
        data: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Prompt:
        return self.request("/accounts/me/prompts/update", body={"promptId": promptId, "data": data}, _auth=_auth)  # type: ignore

    def delete(
        self, promptId: Optional["str"], _auth: Optional[Auth] = None
    ) -> SimpleResponse:
        return self.request(f"/accounts/me/prompts/delete/{promptId}", body={}, _auth=_auth)  # type: ignore


class AccountsMeReactions(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def save(
        self,
        data: Optional["str"],
        skipNotification: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> Reaction:
        return self.request("/accounts/me/reactions/save", body={"data": data, "skipNotification": skipNotification}, _auth=_auth)  # type: ignore


class AccountsMeStates(SNRequest):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def list(
        self,
        _id: Optional["str"],
        limit: Optional["str"],
        skip: Optional["str"],
        sort: Optional["str"],
        filters: Optional["str"],
        _auth: Optional[Auth] = None,
    ) -> StateList:
        return self.request("/accounts/me/states", body={"_id": _id, "limit": limit, "skip": skip, "sort": sort, "filters": filters}, _auth=_auth)  # type: ignore

    def get(self, stateId: Optional["str"], _auth: Optional[Auth] = None) -> State:
        return self.request(f"/accounts/me/states/{stateId}", body={}, _auth=_auth)  # type: ignore

    def save(self, data: Optional["str"], _auth: Optional[Auth] = None) -> State:
        return self.request("/accounts/me/states/save", body={"data": data}, _auth=_auth)  # type: ignore
