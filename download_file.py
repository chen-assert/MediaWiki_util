import urllib.request
import re
import os
import wikia_robot as wr
from urllib.parse import unquote

# 手动指定socks代理
proxy_support = urllib.request.ProxyHandler({'https': 'socks5://127.0.0.1:9542', 'http': 'socks5://127.0.0.1:9542'})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)

urlbase = "https://hoi4.paradoxwikis.com"
dest_page = urlbase + "/Category:Flags"
filebase = urlbase + "/File:"

dir = './output/'


def download(filename):
    need_web = filebase + filename
    response = urllib.request.urlopen(need_web, timeout = 5)
    readed = response.read()
    decoded = readed.decode('utf8')
    file_regex = re.compile(r'(<a\s(href|title)=")(.*?)("\sclass="internal")')
    # why use search in here?
    fileurl0 = file_regex.search(decoded)
    # print(fileurl0.group(3))
    fileurl = urlbase + fileurl0.group(3)
    print(fileurl)
    if not os.path.exists(dir + filename):
        try:
            with urllib.request.urlopen(fileurl, timeout = 10) as response, open(dir + filename, 'wb') as out_file:
                data = response.read()  # a `bytes` object
                out_file.write(data)
            print("File download success")
        except:
            print("File download fail")
    else:
        print("File %s already exist" % filename)


if __name__ == "__main__":
    response = urllib.request.urlopen(dest_page)
    readed = response.read()
    decoded = readed.decode('utf8')
    # href="/File:Al-Andalus.png"
    r = re.compile(r'(/File:)(.*?)("\sclass="gallery)')
    list = r.findall(decoded)
    # print(list)
    num = 0
    for l in list:
        num += 1
        print("Download file %s(%d/%d)" % (l[1], num, len(list)))
        try:
            download(l[1])
        except Exception as e:
            print(e)

        # repair(l[1])

    # path = "./output/"
    # files = os.listdir(path)
    # for name in files:
    #     print("upload " + path + "/" + name)
    #     wr.upload(name, path)
