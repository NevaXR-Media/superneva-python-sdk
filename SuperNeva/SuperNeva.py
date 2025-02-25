from SuperNeva.SNLogger import SNLogger
from SuperNeva.SNConfig import SNConfig
from SuperNeva.SNSQS import SNSQS
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


class SuperNeva:
    def __init__(self, config: SNConfig) -> None:
        self.config = config
        self.logger = SNLogger(name="SuperNeva", colorize=False)

        self.base_url = config["base_url"]
        self.public = config["public"]

        self.isSuperNevaReady = config["base_url"] != ""
        self.isResponseQueueReady = config["sqs_config"] is not None

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
