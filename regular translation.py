import csv
import os
import re
import json

#file_list = ["text1.csv", "India.csv", "HolyFury.csv"]
file_list = None
#<span style="color:red">此项设置将导致成就无效！</span>
w = re.compile(r'(.*\|)(.*?)(<span.*?\n)')
#w = re.compile(r'({{(.*?\|){2})(.*?)(\|)')#1,3,4
group_num_front=1
group_num_mid=2
group_num_back=3
#todo:cache
def myopen(path, type="json"):
    re_list = list()
    files_zh = os.listdir(path)  # 得到文件夹下的所有文件名称
    for name in files_zh:  # 遍历文件夹
        print(path + "/" + name)
        if (not os.path.isdir(path + "/" + name)) and (file_list == None or name in file_list):  # 判断是否是文件夹，不是文件夹才打开
            file = open(path + "/" + name, "r", encoding='UTF-8')
            if type == "csv":
                reader = csv.reader(file, delimiter=";")
                re_list.extend(list(reader))
            elif type == "json":
                reader = json.load(file)
                for i in reader:
                    re_list.append([i['key'], i['original'], i['translation']])
            file.close()
        elif os.path.isdir(path + "/" + name):
            re_list.extend(myopen(path + "/" + name))
    return re_list


#path = "./data/eu4raw"  # 文件夹目录
path = "./data/raw"
tr_raw = myopen(path)

dict_tr = dict()
for i in tr_raw:
    dict_tr[i[1]] = i[2]
    # create map

txtlist = list()
file = open("./data/in.txt", "r", encoding='UTF-8')
for line in file:
    txtlist.append(line)
file.close()


def replace(matched):
    str = matched.group(group_num_mid)
    str=str.strip()
    # print(str)
    if dict_tr.__contains__(str):
        #return matched.group(group_num_front) +"{{ruby|"+ dict_tr[str]+"|"+str+"}}" + matched.group(group_num_back)
        return matched.group(group_num_front) + dict_tr[str] + matched.group(group_num_back)
    else:
        return matched.group(0)


for i in range(len(txtlist)):
    txtlist[i] = w.sub(lambda x: replace(x), txtlist[i])

file = open("./data/out.txt", "w", encoding='UTF-8')
for i in txtlist:
    print(i, file=file, end='')
file.close()
