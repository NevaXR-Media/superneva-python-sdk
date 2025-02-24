from typing import Any, Optional, TypedDict
import requests
import boto3  # type: ignore
from SuperNeva.SNLogger import SNLogger
from SuperNeva.SuperNevaAPI import (
    SNInfo,
    SNInterests,
    SNLogs,
    SNMetas,
    SNPrompts,
    SNReactions,
    SNTargets,
    SNFiles,
    SNCollections,
    SNContents,
    SNAccounts,
    SNAuth,
)


class Auth(TypedDict, total=False):
    account_id: Optional[str]
    token: Optional[str]
    provider: Optional[str]


class SQSConfig:
    region: str
    secret: str
    key: str
    url: str

    def __init__(self, region: str, secret: str, key: str, url: str) -> None:
        self.region = region
        self.secret = secret
        self.key = key
        self.url = url


class SNConfig:
    base_url: str
    public: str
    sqs_config: Optional[SQSConfig]

    def __init__(
        self, base_url: str, public: str, sqs_config: Optional[SQSConfig] = None
    ) -> None:
        self.base_url = base_url
        self.public = public
        self.sqs_config = sqs_config


class SNRequest:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SNRequest", colorize=False)
        self.base_url = config.base_url
        self.public = config.public

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


class SNSQS:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SuperNeva", colorize=False)
        self.base_url = config.base_url
        self.public = config.public
        self.sqs: Any = None

        if config.sqs_config is None:
            self.logger.warning("SQS is not set")

        else:
            self.region_name = config.sqs_config.region
            self.aws_secret_access_key = config.sqs_config.secret
            self.aws_access_key_id = config.sqs_config.key
            self.url = config.sqs_config.url

            self.sqs = boto3.client(  # type: ignore
                "sqs",
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            )

    def push(self, body: Any, groupId: str, deduplicationId: str) -> None:
        if self.sqs is None:
            self.logger.warning("SQS is not set")
            return

        self.logger.info("Pushing message to SQS")
        self.sqs.send_message(  # type: ignore
            QueueUrl=self.url,
            MessageBody=body,
            MessageGroupId=groupId,
            MessageDeduplicationId=deduplicationId,
        )


class SuperNeva:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SuperNeva", colorize=False)

        self.base_url = config.base_url
        self.public = config.public

        self.isSuperNevaReady = config.base_url != ""
        self.isResponseQueueReady = config.sqs_config is not None

        self.queue = SNSQS(config)
        self.prompts = SNPrompts(config)
        self.targets = SNTargets(config)
        self.reactions = SNReactions(config)
        self.metas = SNMetas(config)
        self.logs = SNLogs(config)
        self.interests = SNInterests(config)
        self.info = SNInfo(config)
        self.files = SNFiles(config)
        self.contents = SNContents(config)
        self.collections = SNCollections(config)
        self.auth = SNAuth(config)
        self.accounts = SNAccounts(config)
