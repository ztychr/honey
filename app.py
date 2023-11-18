from flask import Flask, request, render_template, send_file, abort
from urllib.parse import urlparse
from datetime import datetime
import json, requests

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    date = datetime.now()
    timestamp = datetime.timestamp(date)
    user_agent = request.headers.get('User-Agent')
    ip = request.headers.get('X-Real-Ip')
    group = request.args.get('group').strip("\\")
    idx = request.args.get('id').strip("\\")
    src = request.args.get('src')
    filename = request.args.get('filename')
    info = json.loads(requests.get("http://ip-api.com/json/%s" % ip).text)

    if not check_entry(group, idx, src, filename):
        abort(401)
    
    data = {
        "id": idx,
        "group": group,
        "src": src,
        "data":
        {
            "filename": filename, 
            "date": str(date),
            "timestamp": str(timestamp),
            "User-Agent": user_agent,
        },
        "whois": info,
    }
    
#    if src == "qr":
#        with open('data/%s.qr.json' % group, 'a', encoding='utf-8') as f:
#            json.dump(data, f, ensure_ascii=False, indent=4)
#    else:
#        with open('data/%s.drive.json' % group, 'a', encoding='utf-8') as f:
#            json.dump(data, f, ensure_ascii=False, indent=4)

    if src == "qr":
        file_path = 'data/%s.qr.json' % group
    else:
        file_path = 'data/%s.drive.json' % group
        
    try:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = { "boeing": [] }
        print(existing_data)

    if group in existing_data:
        existing_data[group].append(data)
    else:
#        existing_data[group] = [append(data)]
        existing_data[group].append(data)

    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)
    
    #print(json.dumps(data, indent=4))
    return render_template("index.da.html")

@app.route("/info", methods=['GET'])
def boeing():
    group = request.headers.get("group")
    return render_template("index.da.html")
    
def check_entry(group, idx, src, filename):
    try:
        with open('entries/%s.entries.json' % group, 'r', encoding='utf-8') as f:
            entries = json.load(f)
    except FileNotFoundError:
        return abort(418)
    
    if idx in entries:
        for entry in entries[idx]:
            if (entry.get('group') == group and
                entry.get('src') == src and
                entry.get('filename') == filename):
                print("Entry OK")
                return True
    print("Entry NOT OK")
    return False
    
