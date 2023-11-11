from lib.msword import make_canary_msword
from lib.msexcel import make_canary_msexcel
from random import choice
from string import ascii_uppercase, ascii_lowercase
import urllib.parse, os

base_url = 'http://localhost:5000/'
#print(url + urllib.parse.urlencode(params))

LANG="DA"

data = {
    "boing": 1,
}

layout = {
    "Pictures": [
        "p1",
        "p2",
        "p3",
        "p4",
        "p5"
    ],
    "Documents": [
        "d1",
        "d2",
    ],
}

def main(LANG, data, layout, base_url):
    for group in data:
        for i in range(data[group]):
            idx = ''.join(choice(ascii_uppercase+ascii_lowercase) for i in range(12))
            params = {"group": group, "id": idx, "src": "html"}
            url=base_url + urllib.parse.urlencode(params)
        
            for folder in layout:
                if not os.path.exists("output/%s/%s/%s" % (group, idx, folder)):
                    os.makedirs("output/%s/%s/%s" % (group, idx, folder))

                for filex in layout[folder]:
                    if folder == "Pictures":
                        with open("templates/index.da.html", "r") as f:
                            data = f.read() 
                            data = data.replace("REPLACE", url) 
                
                        with open("output/%s/%s/%s/%s.jpg.html" % (group, idx, folder, filex), "w") as file: 
                            file.write(data) 

                        
#                    print(folder, filex)

#                print(i, layout[i][0])
            


"""
    for group in data:
        for i in range(data[group]):
            idx = ''.join(choice(ascii_uppercase+ascii_lowercase) for i in range(12))
            if not os.path.exists("output/%s" % idx):
                os.makedirs("output/%s" % idx)

            params = {"group": group, "id": idx}
            url=base_url + urllib.parse.urlencode(params)

            with open("output/%s/testdoc-%s-%s.docx" % (idx, group, idx), "wb") as f:
                f.write(
                    make_canary_msword(
                        url=url,
                        template="templates/template.docx",
                    )
                )
            with open("output/%s/testdoc-%s-%s.xlsx" % (idx, group, idx), "wb") as f:
                f.write(
                    make_canary_msexcel(
                        url=url,
                        template="templates/template.docx",
                    )
                )
"""
if __name__ == "__main__":
    main(LANG, data, layout, base_url)
