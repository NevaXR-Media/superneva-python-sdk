from typing import Any, TypedDict, Optional

from SuperNeva.SNLogger import SNLogger

import boto3  # type: ignore


class SNSQSConfig(TypedDict):
    region: str
    secret: str
    key: str
    url: str


class SNSQS:
    def __init__(self, config: Optional[SNSQSConfig] = None) -> None:
        self.config = config
        self.logger = SNLogger(name="SuperNeva", colorize=False)
        self.sqs: Any = None

        if config is None:
            self.logger.warning("SQS is not set")

        else:
            self.region_name = config["region"]
            self.aws_secret_access_key = config["secret"]
            self.aws_access_key_id = config["key"]
            self.url = config["url"]

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
