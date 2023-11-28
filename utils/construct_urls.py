import os, sys, json, urllib.parse

file_path = sys.argv[1]

base_url = "https://pid.dk/?"

with open(file_path, "r") as f:
    entries = json.load(f)
    for i in entries:
        files = entries[i]
        for params in files:
            url = base_url + urllib.parse.urlencode(params)
            print(url)
