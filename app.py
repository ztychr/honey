from flask import Flask, request, render_template, send_file, abort
from urllib.parse import urlparse
from datetime import datetime
import json, requests

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    process_request(request)
    return render_template("index.da.html")


@app.route("/en/", methods=["GET"])
def index_da():
    process_request(request)
    return render_template("index.html")


def process_request(request):
    date = datetime.now()
    timestamp = datetime.timestamp(date)
    user_agent = request.headers.get("User-Agent")
    ip = request.headers.get("X-Real-Ip")
    try:
        group = request.args.get("group").strip("\\")
        typex = request.args.get("type").strip("\\")
        idx = request.args.get("id").strip("\\")
        src = request.args.get("src")
        filename = request.args.get("filename")
        info = json.loads(requests.get("http://ip-api.com/json/%s" % ip).text)
        del info['query']
    except:
        abort(401)

    if src == "qr":
        if not check_entry_qr(group, idx, src):
            abort(401)
    else:
        if not check_entry_usb(group, idx, src, filename, typex):
            abort(401)

    data = {
        "id": idx,
        "group": group,
        "src": src,
        "type": typex,
        "data": {
            "filename": filename,
            "date": str(date),
            "timestamp": str(timestamp),
            "User-Agent": user_agent,
        },
        "whois": info,
    }

    if src == "qr":
        file_path = "data/%s.qr.results.json" % group
    else:
        file_path = "data/%s.usb.results.json" % group

    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {group: []}

    existing_data[group].append(data)

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

    print(json.dumps(data, indent=1))


"""    
    if src == "qr":
        with open('data/%s.qr.json' % group, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        with open('data/%s.drive.json' % group, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    return render_template("index.da.html")
"""


def check_entry_usb(group, idx, src, filename, typex):
    try:
        with open("data/%s.usb.entries.json" % group, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except FileNotFoundError:
        return abort(401)

    if idx in entries:
        for entry in entries[idx]:
            if (
                entry.get("group") == group
                and entry.get("src") == src
                and entry.get("filename") == filename
                and entry.get("type") == typex
            ):
                print("Entry OK")
                return True

    print("Entry NOT OK")
    return False


def check_entry_qr(group, idx, src):
    try:
        with open("data/%s.qr.entries.json" % group, "r", encoding="utf-8") as f:
            entries = json.load(f)
    except FileNotFoundError:
        return abort(401)

    if idx in entries:
        for entry in entries[idx]:
            if entry.get("group") == group and entry.get("src") == src:
                print("Entry OK")
                return True

    print("Entry NOT OK")
    return False
