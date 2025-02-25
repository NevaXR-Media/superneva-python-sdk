from typing import Any, TypedDict

from SuperNeva.SNConfig import SNConfig
from SuperNeva.SNLogger import SNLogger

import boto3  # type: ignore


class SNSQSConfig(TypedDict):
    region: str
    secret: str
    key: str
    url: str


class SNSQS:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SuperNeva", colorize=False)
        self.base_url = config["base_url"]
        self.public = config["public"]
        self.sqs: Any = None

        if config["sqs_config"] is None:
            self.logger.warning("SQS is not set")

        else:
            self.region_name = config["sqs_config"]["region"]
            self.aws_secret_access_key = config["sqs_config"]["secret"]
            self.aws_access_key_id = config["sqs_config"]["key"]
            self.url = config["sqs_config"]["url"]

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
