import requests
import json


def get_auth_token(client_id, client_secret):
    token_url = "https://api.amazon.com/auth/O2/token"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    body = dict(
        grant_type="client_credentials",
        scope="messaging:push",
        client_id=client_id,
        client_secret=client_secret
    )
    resp = requests.post(token_url, data=body, headers=headers)
    if resp.status_code != 200:
        print("Crapsticks!", resp)
    return resp.json()


def send_message(auth_info, reg_id, message):
    send_url = ("https://api.amazon.com/messaging/"
                "registrations/{}/messages".format(reg_id))
    body = {
        "data": message,
        "consolidationKey": "simplepush",
        "expiresAfter": 300
    }
    headers = {
        "Authorization": "Bearer {}".format(auth_info["access_token"]),
        "Content-Type": "application/json",
        "X-Amzn-Type-Version": "com.amazon.device.messaging.ADMMessage@1.0",
        "X-Amzn-Accept-Type": "com.amazon.device.messaging.ADMSendResult@1.0",
        "Accept": "application/json",
    }
    data = json.dumps(body)
    resp = requests.post(send_url, data=data, headers=headers)
    if resp.status_code != 200:
        print("Crapsticks!", resp)
    return resp.json()


def main():
    with open("creds") as ff:
        creds = json.loads(ff.read())
    auth_info = get_auth_token(
        creds["client_id"],
        creds["client_secret"]
    )
    print(auth_info)
    message = dict(
        message="This is a test message",
        url="https://example.com"
    )
    with open("reg_id") as ff:
        reg_id = ff.read()
    resp = send_message(auth_info, reg_id, message)
    print(resp)


main()
