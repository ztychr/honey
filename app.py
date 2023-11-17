from flask import Flask, request, render_template, send_file
from urllib.parse import urlparse
from datetime import datetime
import json, uuid, requests

# http://127.0.0.1:5000/group=boeing&id=1337&src=docx
# http://127.0.0.1:5000/group=mitnick&id=1337&src=html
# http://127.0.0.1:5000/group=cogwheel&id=1337&src=qr
# http://127.0.0.1:5000/group=cogwheel&id=1337&src=docx-html

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

    # For running through a proxied vpn-tunnel
#    x_forwarded_for = request.headers.get("X-Forwarded-For")
#    if x_forwarded_for:
#        ip_list = x_forwarded_for.split(",")
#        ip = ip_list[0]
            
    data = {
        "id": idx,
        "group": group,
        "src": src,
        #"type": typex,
        "data":
        {
            "filename": filename, 
            "date": str(date),
            "timestamp": str(timestamp),
            "User-Agent": user_agent,
        },
        "whois": info,
    }

    if src == "qr":
        with open('data/%s.qr.json' % group, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        with open('data/%s.drive.json' % group, 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(json.dumps(data, indent=4))
    return render_template("index.da.html")

@app.route("/info", methods=['GET'])
def boeing():
    group = request.headers.get("group")
    return render_template("index.da.html")
    
    
"""
#"ip": ip,
#"Accept": accept,
#"Accept-Language": accept_la,
#"Accept-Encoding": accept_en,

accept = request.headers.get('Accept')
accept_la = request.headers.get('Accept-Language')
accept_en = request.headers.get('Accept-Encoding')
print(request.environ['REMOTE_ADDR'])
print(request.environ.get('HTTP_X_REAL_IP'))
print(request.environ.get('HTTP_X_FORWARDED_FOR'))
        
    if request.method == 'POST':
        data = request.json
        print(data)
        with open('data.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print("token registeret")

    return "OK"
"""
