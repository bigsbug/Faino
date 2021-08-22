import json
import requests

address_get_token = "https://testwbs.pagekite.me/api/token"
address_verify_token = "https://testwbs.pagekite.me/api/token/verify"
address_refresh = "https://testwbs.pagekite.me/api/token/refresh"
address_devices = "https://testwbs.pagekite.me/devices/"
address_info_user = "https://testwbs.pagekite.me/info_user/"
adsress_data = "https://testwbs.pagekite.me/data/"
adsress_status = "https://testwbs.pagekite.me/status"
# adress_ = 'http://127.0.0.1:8000/'
# refresh = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNTk3Mzc0MCwianRpIjoiZGFkMmQyNzZlOTUyNDNhMTg2M2Q0MGFhNGEzM2UzZDMiLCJ1c2VyX2lkIjoxfQ.cE04wJ4td_CSK3o6sM-eynHZvhW8Hq22TR9W4YTv5Rw'
# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoic2xpZGluZyIsImV4cCI6MTYyNTg4ODQ3MSwianRpIjoiYjNhNGFkMGUxNmZmNDBmMDk4ODliNjc2MmJjMGMxM2UiLCJyZWZyZXNoX2V4cCI6MTYyNTk3NDU3MSwidXNlcl9pZCI6MX0.W5Pr6W12s-_tivVFeiFCxx1N4NrRH0nFKl6U84rb7cA'


def GetToken(username, password):
    site = requests.post(address_get_token,
                         data={
                             "username": username,
                             "password": password
                         })
    return site.json()


def verify(token):
    site = requests.post(address_verify_token, data={"token": token})
    return site.json() == {}


def Test_auth(address, token, data={}, method="get"):
    if method == "get":
        site = requests.get(address,
                            headers={"Authorization": f"JWT {token}"},
                            data=data)
    else:
        site = requests.post(address,
                             headers={"Authorization": f"JWT {token}"},
                             data=data)
    print(site.text)


username = ["nova", "SUPERNOVA"]
password = ["novaman", "nova_man"]


def extract(x):
    return (username[x], password[x])


token = GetToken(*extract(1))["access"]

# print(token)ٍ
# print(verify(token))

Test_auth(adsress_data, token,
          {"token": "3f6eb294-f932-45e6-a888-5c6bd2822179"}, "post")
# Test_auth(address_devices,token,{"token":"ddf05bb8-b5c8-477e-af32-877fb81d3710"},'post')
