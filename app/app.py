from flask import Flask, request, render_template, send_file
from urllib.parse import urlparse
from datetime import datetime
import json, uuid

app = Flask(__name__)

@app.route("/honey", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        date = datetime.now()
        timestamp = datetime.timestamp(date)
        user_agent = request.headers.get('User-Agent')
        ip = request.remote_addr
        accept = request.headers.get('Accept')
        accept_la = request.headers.get('Accept-Language')
        accept_en = request.headers.get('Accept-Encoding')
        idx = request.args.get('id')
        #uuidx = request.uuid.uuid4()
        
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            ip_list = x_forwarded_for.split(",")
            ip = ip_list[0]
            
#        print(request.environ['REMOTE_ADDR'])
#        print(request.environ.get('HTTP_X_REAL_IP'))
#        print(request.environ.get('HTTP_X_FORWARDED_FOR'))
        
        data = {
            "id": idx,
            "data":
            {
                "date": str(date),
                "timestamp": str(timestamp),
                "ip": ip,
                "User-Agent": user_agent,
                "Accept": accept,
                "Accept-Language": accept_la,
                "Accept-Encoding": accept_en,
            }
        }

        with open('tokens.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(data)
        #return send_file('payments.js')
        return "OK"
        
    if request.method == 'POST':
        data = request.json
        print(data)
        with open('data.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print("token registeret")

    return "OK"
    
