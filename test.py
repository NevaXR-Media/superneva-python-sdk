print("Hello, World!")

from SuperNeva.SuperNeva import SuperNeva

sn = SuperNeva(
    config={
        "base_url": "http://localhost:5002/api/v1/",
        "public": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50SWQiOiI2NmUxYzNhNzFhN2FjMzIwOTBkZmQ4ZTIiLCJjcmVhdGVkQnkiOiI2NmUxYzNhNzFhN2FjMzIwOTBkZmQ4ZTIiLCJkZXNjcmlwdGlvbiI6IjEiLCJuYW1lIjoiMSIsInNjb3BlIjp7InRhcmdldHMiOltdLCJlbmRwb2ludHMiOlt7Il9pZCI6Ii9hcGkvdjEvKiIsInBhdGgiOiIvYXBpL3YxLyoifSx7Il9pZCI6Ii9hcGkvdjEvYWNjb3VudHMvbWUvaW50ZXJlc3RzL2RlbGV0ZS86aW50ZXJlc3RJZCIsInBhdGgiOiIvYXBpL3YxL2FjY291bnRzL21lL2ludGVyZXN0cy9kZWxldGUvOmludGVyZXN0SWQifV0sIm9wZXJhdGlvbnMiOlt7Il9pZCI6IioiLCJuYW1lIjoiKiJ9LHsiX2lkIjoiX2FjY291bnQiLCJuYW1lIjoiX2FjY291bnQifV0sImltcGVyc29uYXRpb24iOnsic2VydmljZXMiOlsibmV2YSIsInRydWlkIl0sInJlcXVpcmVUb2tlbiI6dHJ1ZX19LCJpYXQiOjE3MzIwMjQ1MTF9.WvoYO8V6_CNh4krF5GCf78K-v45zo-9grZ_A6VRByKE",
        "sqs_config": {
            "region": "us-east-1",
            "secret": "1234567890",
            "key": "1234567890",
            "url": "https://sqs.us-east-1.amazonaws.com/1234567890/test",
        },
    }
)


print(sn.isSuperNevaReady)

response = sn.metas.create(
    data=[
        {
            "key": "TEST",
            "targets": ["66a37935c7fa10d916f0452e"],
            "type": "DEMO",
            "label": {"en": "Test En"},
        }
    ],
    _auth={"account_id": "668ea11c86cb822019aa3ef6"},
)
# {"data":[{"key":"TEST","targets":["66a37935c7fa10d916f0452e"],"type":"DEMO","label":{"en":"Test En"}}]}
print(response)
