from typing import Any, Optional, TypedDict

from SuperNeva.SNConfig import SNConfig
from SuperNeva.SNLogger import SNLogger

import requests


class Auth(TypedDict, total=False):
    account_id: Optional[str]
    token: Optional[str]
    provider: Optional[str]
    method: Optional[str]


class SNRequest:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SNRequest", colorize=False)
        self.base_url = config["base_url"]
        self.public = config["public"]
        self.secret = config["secret"]

    def request(
        self,
        path: str,
        body: Any,
        auth: Optional[Auth] = None,
    ) -> Any:
        print("NEW REQUEST", self.base_url + path, auth)

        headers = {
            "content-type": "application/json",
        }

        if auth:
            method = auth.get("method")

            if method == "secret" and self.secret:
                headers = {
                    "x-secret-key": self.secret,
                }

            elif self.public:
                headers = {
                    "x-public-key": self.public,
                }

            provider = auth.get("provider", "neva")
            account_id = auth.get("account_id")
            token = auth.get("token")

            if account_id:
                if token:
                    headers["x-impersonate"] = f"{provider}:::{account_id}:::{token}"
                else:
                    headers["x-impersonate"] = f"{provider}:::{account_id}"

        try:
            response = requests.post(self.base_url + path, headers=headers, json=body)
            return response.json()
        except Exception as e:
            self.logger.error("Request failed: " + path)
            return {
                "errors": [
                    {
                        "message": "Request failed",
                        "raw": str(e),
                    }
                ]
            }
