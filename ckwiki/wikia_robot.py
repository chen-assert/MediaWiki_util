import time
import requests

ck2URL = "https://ck2.parawikis.com/api.php"
ck2enURL = "https://ck2.paradoxwikis.com/api.php"
eu4URL = "https://www.eu4cn.com/api.php"
URL = ck2URL
enURL=ck2enURL
S = requests.Session()
CSRF_TOKEN = None
password_ck2 = "hq4lunoqglja05olua15trg104d3gq0v"
password_eu4 = "3dliq7j27elp13f1qbmglr85q3obrg04"
password = password_ck2
proxydict = {'https': 'socks5://127.0.0.1:9542', 'http': 'socks5://127.0.0.1:9542'}
#S.proxies.update(proxydict)

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
    # Send a post request to login. Using the main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        'action': "login",
        'lgname': "忆九歌@忆九歌-robot",
        'lgpassword': password,
        'lgtoken': LOGIN_TOKEN,
        'format': "json"
    }

    R = S.post(URL, data=PARAMS_1)
    DATA2 = R.json()
    # print(DATA2)
    # Step 3: Obtain a CSRF token
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
    # Step 4: POST request to upload a file directly
    PARAMS_4 = {
        "action": "upload",
        "filename": filename,
        "format": "json",
        "token": CSRF_TOKEN,
        "text": "== 授权协议 == \n {{C-Paradox}}"
    }
    FILE = {'file': (filename, open(path + filename, 'rb'), 'multipart/form-data')}
    R = S.post(URL, files=FILE, data=PARAMS_4)
    DATA = R.json()
    print(DATA)
def create(pagename, content):
    PARAMS = {
        "action": "edit",
        "title": pagename,
        "format": "json",
        "token": CSRF_TOKEN,
        "ignorewarnings": 1,
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
