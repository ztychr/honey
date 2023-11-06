from lib.msword import make_canary_msword
from lib.msexcel import make_canary_msexcel
from random import choice
from string import ascii_uppercase, ascii_lowercase
import urllib.parse, os

base_url = 'http://localhost:5000/?group=red&id=id'
#print(url + urllib.parse.urlencode(params))

data = {
    "blue": 2,
}

#for i in data:
#    print(i, data[i])

def make_docx(idx, url):
    with open("output/%s/Documents/resume.docx" % (idx), "wb") as f:
        f.write(
            make_canary_msword(
                url=url,
                template="/home/user/honey/utils/templates/template.docx",
            )
        )

def make_xlsx(idx, url):
    with open("output/%s/Notes/payslip.xlsx" % (idx), "wb") as f:
        f.write(
            make_canary_msexcel(
                url=url,
                template="/home/user/honey/utils/templates/template.docx",
            )
        )
        
def main(data):
    for group in data:
        for i in range(data[group]):
            idx = ''.join(choice(ascii_uppercase+ascii_lowercase) for i in range(12))
            if not os.path.exists("output/%s" % idx):
                os.makedirs("output/%s" % idx)
                os.makedirs("output/%s/Documents" % idx)
                os.makedirs("output/%s/Notes" % idx)

            params = {"group": group, "id": idx}
            url=base_url + urllib.parse.urlencode(params)

            make_docx(idx, url)
            make_xlsx(idx, url)

            print(url)

if __name__ == "__main__":
    main(data)
