from lib.msword import make_canary_msword
from lib.msexcel import make_canary_msexcel
from random import choice
from string import ascii_uppercase, ascii_lowercase
from datetime import datetime
import urllib.parse, os, random

base_url = 'http://nordskov.net:8080/?'
#print(url + urllib.parse.urlencode(params))

LANG="DA"

data = {"boing": 1}

layout = {
    "Christmas Party": [
        "IMG_2622.jpg",
        "IMG_2623.jpg",
        "IMG_2624.jpg",
        "IMG_2625.jpg",
        "IMG_2626.jpg",
        "IMG_2627.jpg",
        "IMG_2628.jpg",
        "IMG_2629.jpg",
        "IMG_2630.jpg",
        "IMG_2631.jpg",
    ],
    
    "Important Docs": [
        "Meeting-Notes.docx",
        "Payslip-October.docx",
        "Budget-OLD.xlsx",
        "Budget-2024.xlsx",
        "Resume.pdf",
        "Resume-new.pdf",
        "Performance-Appraisal.pdf"
    ]
}

def main(LANG, data, layout, base_url):
    for group in data:
        for i in range(data[group]):
            idx = ''.join(choice(ascii_uppercase+ascii_lowercase) for i in range(12))
            params = {"group": group, "id": idx}
        
            for folder in layout:
                if not os.path.exists("output/%s" % folder):# and not folder == "Root":
                    os.makedirs("output/%s" % folder)
                    time = gen_time(sync=False)
                    os.utime("output/%s" % folder, (time, time))

                for filex in layout[folder]:
                    file_type = filex.rsplit('.', 1)[-1]# for x in la]
                    if file_type == "jpg":
                        params["src"] = "html"
                        url=base_url + urllib.parse.urlencode(params)
                        make_html(filex, folder, url)
                    elif file_type == "docx":
                        params["src"] = "docx"
                        url=base_url + urllib.parse.urlencode(params).replace("&", "&amp;")
                        make_docx(filex, folder, url)
                    elif file_type == "xlsx":
                        params["src"] = "xlxs"
                        url=base_url + urllib.parse.urlencode(params).replace("&", "&amp;")
                        make_xlsx(filex, folder, url)
                    elif file_type == "pdf":
                        params["src"] = "pdf"
                        url=base_url + urllib.parse.urlencode(params)
                        make_html(filex, folder, url)

def make_html(file_name, path, url):
    with open("templates/index.da.html", "r") as f:
        data = f.read() 
        data = data.replace("REPLACE", url)               
    with open("output/%s/%s.html" % (path, file_name), "w") as file:
        file.write(data)
    time = gen_time(sync=True) if ".jpg" in file_name else gen_time(sync=False)
    os.utime(file.name, (time, time))

def make_docx(file_name, path, url):
    with open("output/%s/%s" % (path, file_name), "wb") as f:
        f.write(
            make_canary_msword(
                url=url,
                template="/home/user/thesis/honey/utils/templates/template.docx",
            )
        )
    time = gen_time(sync=False)
    os.utime(f.name, (time, time))

def make_xlsx(file_name, path, url):
    with open("output/%s/%s" % (path, file_name), "wb") as f:
        f.write(
            make_canary_msexcel(
                url=url,
                template="templates/template.xlsx",
            )
        )
    time = gen_time(sync=False)
    os.utime(f.name, (time, time))


def gen_time(sync: bool):
    time = 1699583472 if sync else random.randint(1698796800, 1699920000)
    return time

if __name__ == "__main__":
    main(LANG, data, layout, base_url)

