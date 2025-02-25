from typing import Optional, TypedDict

from SuperNeva.SNSQS import SNSQSConfig


class SNConfig(TypedDict):
    base_url: str
    public: str
    sqs_config: Optional[SNSQSConfig]
