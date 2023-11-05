from flask import Flask, request, render_template, send_file
from urllib.parse import urlparse
from datetime import datetime
import json, uuid, requests

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
        group = request.args.get('group')

        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            ip_list = x_forwarded_for.split(",")
            ip = ip_list[0]
#            for i in ip_list:
#                print("IP: ", ip)
            info = json.loads(requests.get("http://ip-api.com/json/%s" % ip).text)
#            print(json.dumps(info, indent=4))


        data = {
            "group": group,
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
            },
            "whois": info,
        }

        with open('tokens.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

            for i in request.headers:
                print(i)
#        print(request.environ['REMOTE_ADDR'])
#        print(request.environ.get('HTTP_X_REAL_IP'))
#        print(request.environ.get('HTTP_X_FORWARDED_FOR'))

        print(json.dumps(data, indent=4))
        return "OK"
        #return send_file('payments.js')
        
    if request.method == 'POST':
        data = request.json
        print(data)
        with open('data.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print("token registeret")

    return "OK"
    
