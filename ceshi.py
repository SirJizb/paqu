import requests
import bs4
from bs4 import BeautifulSoup

def getHTMLText(url):  # 通用代码框架
    try:
        kv = {'user-agent': 'Mozilla/5.0'}  # 模拟浏览器向页面发起请求
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()  # 如果不是200， 引发HTTPError异常
        r.encoding = r.apparent_encoding  # 应用内容分析出的编码形式
        print("访问成功\n")
        return r.text  # 返回网页内容字符串形式
    except:
        return "产生异常"
# 根据国名查询信息
def chosecountry(country):
    li2 = []  # 存放输出信息
    flag = 0
    for tag1 in li:
        for i1 in tag1.children:
            if isinstance(i1, bs4.element.Tag):
                if i1.string == country:
                    flag = 1
                    for i2 in tag1.children:
                        if isinstance(i2, bs4.element.Tag):
                            if i2.attrs["class"][0] == "cured-notag":
                                li2.append(i2.string)
                                print(mat.format("国家", "确诊", "死亡", "治愈"))
                                print(mat.format(li2[0], li2[1], li2[2], li2[3]))
                            else:
                                li2.append(i2.string)
    if flag == 0:
        print("该国家没有疫情情况或输入国家名有误")
    else:
        pass
# 查询所有国家疫情信息
def searchall():
    list1 = []
    number = 0  # 计算国家数目
    for tag2 in li:
        for i3 in tag2.children:
            if isinstance(i3, bs4.element.Tag):
                if i3.attrs["class"][0] == "cured-notag":
                    list1.append(i3.string)
                    print(mat.format(list1[0], list1[1], list1[2], list1[3]))
                    list1 = []
                    number += 1
                else:
                    list1.append(i3.string)
    print("\n目前共有 "+str(number)+" 个国家存在疫情情况")


# 解析网页
html = getHTMLText('http://m.sinovision.net/newpneumonia.php')
soup = BeautifulSoup(html, 'html.parser')
# 获取时间和总数
timetag = soup.find_all("span", attrs={"class": "today-time"})[3]
print(timetag.string + '\n')  # 时间
tag = soup.find("div", attrs={"class": "recentNumber other-area"})
ulist = []  # 总数
for child in tag.children:
    if isinstance(child, bs4.element.Tag):
        for i in child.children:
            if isinstance(i, bs4.element.Tag):
                ulist.append(i.string)
mat0 = "{:4}\t{:4}\t{:4}\t{:4}"
print(mat0.format(ulist[-1], ulist[-2], ulist[-3], ulist[-4]))

print("#" * 50)


# 解析国家详情
mat = "{:8}\t{:4}\t{:4}\t{:4}"  # 输出格式
li = []  # 所有国家信息
html1 = html[html.find("<div class=\"todaydata morecontent\">"):
             html.find("<div class=\"todaydata morecountry\">")]
soup1 = BeautifulSoup(html1, "html.parser")
li = soup1.find_all("div", attrs={"class": "prod"})
# 将所有国家的信息存放在li列表中

# 选择查询方式
active = True
while active:
    print("\n"+'#'*50)
    country = input("请输入国家名字/ 输入q结束/ 输入all查询所有 \n input: ")
    if country == 'q':
        active = False
    elif country == "all":
        searchall()
    else:
        chosecountry(country)