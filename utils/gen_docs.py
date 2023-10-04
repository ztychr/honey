from lib.msword import make_canary_msword
from lib.msexcel import make_canary_msexcel
from random import choice
from string import ascii_uppercase, ascii_lowercase
import urllib.parse, os

base_url = 'https://nordskov.net/honey?'
#print(url + urllib.parse.urlencode(params))

data = {
    "blue": 3,
    "red": 4,
}

#for i in data:
#    print(i, data[i])

def main(data):
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
                        template="/home/user/honey/utils/templates/template.docx",
                    )
                )
            with open("output/%s/testdoc-%s-%s.xlsx" % (idx, group, idx), "wb") as f:
                f.write(
                    make_canary_msexcel(
                        url=url,
                        template="/home/user/honey/utils/templates/template.docx",
                    )
                )

if __name__ == "__main__":
    main(data)
