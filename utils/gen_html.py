from lib.msword import make_canary_msword
from lib.msexcel import make_canary_msexcel
from random import choice
from string import ascii_uppercase, ascii_lowercase
import urllib.parse, os, random

base_url = 'http://localhost:5000/?'
#print(url + urllib.parse.urlencode(params))

LANG="DA"

data = {"boing": 1}

layout = {
    "Root": [
        "resume.pdf",
        "resume-new.pdf"
    ],
    
    "Pictures": [
        "IMG2622.jpg",
        "IMG2623.jpg",
        "IMG2624.jpg"
    ],
    
    "Documents": [
        "meeting-notes.docx",
        "payslip-october.docx",
        "budget-for-department.xlsx"
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

                for filex in layout[folder]:
                    file_type = filex.rsplit('.', 1)[-1]# for x in la]
                    if file_type == "jpg":
                        params["src"] = "html"
                        url=base_url + urllib.parse.urlencode(params)
                        make_html(filex, folder, url)
                    elif file_type == "docx":
                        params["src"] = "docx"
                        url=base_url + urllib.parse.urlencode(params)
                        make_docx(filex, folder, url)
                    elif file_type == "xlsx":
                        params["src"] = "xlxs"
                        url=base_url + urllib.parse.urlencode(params)
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
        time = gen_time()
    os.utime(file.name, (time, time))

def make_docx(file_name, path, url):
    with open("output/%s/%s" % (path, file_name), "wb") as f:
        f.write(
            make_canary_msword(
                url=url,
                template="templates/template.docx",
            )
        )
    time = gen_time()
    os.utime(f.name, (time, time))

def make_xlsx(file_name, path, url):
    with open("output/%s/%s" % (path, file_name), "wb") as f:
        f.write(
            make_canary_msexcel(
                url=url,
                template="templates/template.docx",
            )
        )
    time = gen_time()
    os.utime(f.name, (time, time))


def gen_time():
    time = random.randint(1694031783, 1696118400)
    return time

if __name__ == "__main__":
    main(LANG, data, layout, base_url)

