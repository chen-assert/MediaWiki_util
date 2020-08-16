import requests
from urllib.parse import unquote

ck2URL = "https://ck2.parawikis.com/api.php"
ck2enURL = "https://ck2.paradoxwikis.com/api.php"
eu4URL = "https://www.eu4cn.com/api.php"
eu4enURL = "https://eu4.paradoxwikis.com/api.php"
URL = ck2URL
enURL = ck2enURL
S = requests.Session()
CSRF_TOKEN = None
name = "忆九歌2"
password = "delete"
proxydict = {'https': 'socks5://127.0.0.1:9542', 'http': 'socks5://127.0.0.1:9542'}


# S.proxies.update(proxydict)

def login():
    print("start logining")
    # Retrieve login token first
    PARAMS_0 = {
        'action': "query",
        'meta': "tokens",
        'type': "login",
        'format': "json"
    }

    R = S.post(url=URL, params=PARAMS_0)
    DATA1 = R.json()

    LOGIN_TOKEN = DATA1['query']['tokens']['logintoken']
    # print(LOGIN_TOKEN)
    PARAMS_1 = {
        'action': "login",
        'lgname': name,
        'lgpassword': password,
        'lgtoken': LOGIN_TOKEN,
        'format': "json"
    }

    R = S.post(URL, data=PARAMS_1)
    DATA2 = R.json()
    # print(DATA2)
    # Obtain a CSRF token
    PARAMS_3 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_3)
    DATA = R.json()
    global CSRF_TOKEN
    CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]
    print("logining successfully")


def upload(filename, path):
    PARAMS = {
        "action": "upload",
        "filename": filename,
        "format": "json",
        "token": CSRF_TOKEN,
        "text": "== 授权协议 == \n {{C-Paradox}}"
    }
    FILE = {'file': (filename, open(path + filename, 'rb'), 'multipart/form-data')}
    R = S.post(URL, files=FILE, data=PARAMS)
    DATA = R.json()
    print(DATA)


def create(pagename, content):
    PARAMS = {
        "action": "edit",
        "title": pagename,
        "format": "json",
        "token": CSRF_TOKEN,
        "text": content,

    }
    R = S.post(URL, PARAMS)
    DATA = R.json()
    print(DATA)


def parse(page):
    PARAMS = {
        "action": "parse",
        "page": page,
        "format": "json",
        "prop": "wikitext"
    }
    R = S.get(url=enURL, params=PARAMS)
    DATA = R.json()
    return DATA
