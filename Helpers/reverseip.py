import requests
import os

BASE_URL = "https://api.viewdns.info/"
REVERSE_IP_URL = BASE_URL + "reverseip/"


class Ip(BaseModel):
    ip: str

class Domain(BaseModel):
    domainName: str

def reverseip(domain: Domain):
    ip = Ip.ip
    params = {"host": ip, "output": "json", "apikey": os.environ.get("VIEWDNS_KEY", "")}
    res = requests.get(REVERSE_IP_URL, params=params)
    return res.json()
