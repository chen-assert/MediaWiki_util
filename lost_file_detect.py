# writed by chenassert 2019/3/25
# todo:上传图片时加入分类
# todo:separate the file upload function
# todox:make gui(give up)
import urllib.request
import re
import os
import wikia_robot as wr
from urllib.parse import unquote

# proxy_support = urllib.request.ProxyHandler({'https': 'socks5://127.0.0.1:9542', 'http': 'socks5://127.0.0.1:9542'})
# 手动指定socks代理
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)
# urlform = "https://eu4.paradoxwikis.com"
# urlto = "https://www.eu4cn.com"
urlform = "https://ck2.paradoxwikis.com"
urlto = "https://ck2.parawikis.com"

# Category:含有受损文件链接的页面
# 使用该页面而不是Special:需要的文件是为了避免分析一些用户私有页面中请求的文件
# dest_page_list = "https://www.eu4cn.com/wiki/Category:%E5%90%AB%E6%9C%89%E5%8F%97%E6%8D%9F%E6%96%87%E4%BB%B6%E9%93%BE%E6%8E%A5%E7%9A%84%E9%A1%B5%E9%9D%A2"
dest_page_list = "https://ck2.parawikis.com/index.php?title=Category:%E5%90%AB%E6%9C%89%E5%8F%97%E6%8D%9F%E6%96%87%E4%BB%B6%E9%93%BE%E6%8E%A5%E7%9A%84%E9%A1%B5%E9%9D%A2"
dir = './output/'


def repair(link):
    need_web = urlto + link
    response = urllib.request.urlopen(need_web)
    readed = response.read()
    decoded = readed.decode('utf8')
    r = re.compile(r'(DestFile=)(.*?)(")')
    list1 = r.findall(decoded)
    list2 = [unquote(i[1]) for i in list1]
    list2 = list(set(list2))
    content = []
    for word in list2:
        restr = urlform + "/File:" + word
        data = wr.parse("File:" + word)
        # print("File:" + word)
        # print(data)
        try:
            if (not data.__contains__("error") and "REDIRECT" in data["parse"]["wikitext"]["*"]):
                print("redirect found in " + "File:" + word + ", try to create the redirect web")
                wr.create("File:" + word, data["parse"]["wikitext"]["*"])
                continue
        except:
            pass
        if not os.path.exists(dir + word):
            print("request to %s " % (restr), end='')
            try:
                response2 = urllib.request.urlopen(restr)
                content.append(response2.read().decode('utf8'))
                print("success")
            except:
                print("fail")
    content2 = []
    r2 = re.compile(r'(<a\s(href|title)=")(.*?)("\sclass="internal")')
    for c in content:
        l = r2.search(c)
        insert = l.group(3)
        if insert not in content2:
            content2.append(insert)

    if not os.path.exists(dir):
        os.makedirs(dir)
    for c in content2:
        # 13是什么?
        if not os.path.exists(dir + c[13:]):
            print("request to %s " % (urlform + c), end='')
            try:
                with urllib.request.urlopen(urlform + c) as response, open(dir + unquote(c[13:]), 'wb') as out_file:
                    data = response.read()  # a `bytes` object
                    out_file.write(data)
                print("success")
            except:
                print("fail")


if __name__ == "__main__":
    wr.login()
    response = urllib.request.urlopen(dest_page_list)
    readed = response.read()
    decoded = readed.decode('utf8')
    r = re.compile(r'(<li><a\shref=")(.*?)("\stitle=)')
    list3 = r.findall(decoded)
    for l in list3:
        if "User" not in l[1]:
            print("repair to page %s" % (l[1]))
            repair(l[1])

    path = "./output/"
    files = os.listdir(path)
    for name in files:
        print("upload " + path + "/" + name)
        wr.upload(name, path)
