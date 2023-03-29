import requests
import pandas as pd
import json

def requestmoex(method: str):
    url = "https://iss.moex.com/iss/engines/futures/markets/options/boards/ROPD/securities.json"
    r = requests.get(url)
    r.encoding = 'utf-8'
    j = r.json()
    return j


def flatten(j: dict, blockname: str):
    return [{str.lower(k): r[i] for i, k in enumerate(j[blockname]['columns'])} for r in j[blockname]['data']]
def main():
    j = requestmoex("securities")
    f = flatten(j, 'securities')
    return f
data = main()


