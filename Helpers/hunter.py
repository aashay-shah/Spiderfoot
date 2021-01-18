import os
import requests

BASE_URL = "https://api.hunter.io/v2/"
DOMAIN_SEARCH_URL = BASE_URL + "domain-search"

def hunter(domain: str):
    domain = domain
    params = {"domain": domain, "api_key": ""}
    res = requests.get(DOMAIN_SEARCH_URL, params=params)
    return res.json()
