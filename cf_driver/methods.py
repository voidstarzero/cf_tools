# Copyright 2020 James Arcus <jimbo@ucc.asn.au>.
# Released under the terms of the GNU GPLv3 or later.

################################################################################

import requests

################################################################################

# Formatting helpers

def PATH(endpoint):
    return "https://api.cloudflare.com/client/v4" + endpoint

def HEADERS(token):
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

def RESULT(response):
    details = response.json()

    if details["success"]:
        return details["result"]
    elif len(details["errors"]) == 1 and details["errors"][0]["code"] == 0:
        return [] # Special case for bad query, unsure why API returns a permisison error
    else:
        raise RuntimeError(repr(details["errors"]))

################################################################################

# Cloudflare API methods

def delete(token, endpoint):
    response = requests.delete(PATH(endpoint), headers=HEADERS(token))
    return RESULT(response)

def get(token, endpoint, query=None):
    response = requests.get(PATH(endpoint), params=query, headers=HEADERS(token))
    return RESULT(response)

def patch(token, endpoint, data):
    response = requests.patch(PATH(endpoint), json=data, headers=HEADERS(token))
    return RESULT(response)

def post(token, endpoint, data):
    response = requests.post(PATH(endpoint), json=data, headers=HEADERS(token))
    return RESULT(response)

def put(token, endpoint, data=None):
    response = requests.put(PATH(endpoint), json=data, headers=HEADERS(token))
    return RESULT(response)
