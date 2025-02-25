print("Hello, World!")

from SuperNeva.SuperNeva import SuperNeva

sn = SuperNeva(
    config={
        "base_url": "https://api.superneva.com",
        "public": "1234567890",
        "sqs_config": {
            "region": "us-east-1",
            "secret": "1234567890",
            "key": "1234567890",
            "url": "https://sqs.us-east-1.amazonaws.com/1234567890/test",
        },
    }
)


print(sn.isSuperNevaReady)
print(sn.isResponseQueueReady)
