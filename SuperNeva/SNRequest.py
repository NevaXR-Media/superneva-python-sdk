from typing import Any, Optional, TypedDict

from SuperNeva.SNConfig import SNConfig
from SuperNeva.SNLogger import SNLogger

import requests


class Auth(TypedDict, total=False):
    account_id: Optional[str]
    token: Optional[str]
    provider: Optional[str]


class SNRequest:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SNRequest", colorize=False)
        self.base_url = config["base_url"]
        self.public = config["public"]

    def request(
        self,
        path: str,
        body: Any,
        auth: Optional[Auth] = None,
    ) -> Any:
        if auth is None:
            headers = {
                "content-type": "application/json",
                "x-public-key": self.public,
            }
        else:
            headers = {
                "content-type": "application/json",
                "x-public-key": self.public,
                "x-impersonate": (
                    auth.get("token")
                    if f"{auth.get('provider')}:::{auth.get('account_id')}:::{auth.get('token')}"
                    else f"{auth.get('provider')}:::{auth.get('account_id')}"
                ),
            }
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
