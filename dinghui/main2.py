import requests
from lxml import etree
import pymysql


def getdata(url):
    # 请求CVPR主页
    page_text = requests.get(url).text
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(page_text, parser=parser)

    # 爬取论文连接
    hrefs = tree.xpath('//dt[@class="ptitle"]/a/@href')
    print(len(hrefs))

    # 爬取论文信息
    titles = []
    pdfs = []
    abstracts = []
    authors = []
    keywords = []

    for href in hrefs:
        db = pymysql.connect(host="localhost", user="root", password="123456",
                             database="db")

        href = "https://openaccess.thecvf.com/" + href
        page_text = requests.get(href).text
        tree_link = etree.HTML(page_text, parser=parser)

        title = tree_link.xpath('/html/body/div/dl/dd/div[@id="ptitle"]/text()')
        title[0] = title[0].strip()
        titles += title

        title[0] = title[0].replace(":", "")
        words = title[0].split()
        keyword = ""
        for word in words:
            if checkword(word):
                save_keywords(pymysql.connect(host="localhost", user="root", password="123456",
                                              database="db"), word)
                keyword += word + " "

        keywords.append(keyword)

        pdf = tree_link.xpath('/html/body/div/dl/dd/a[contains(text(),"pdf")]/@href')
        pdf[0] = pdf[0].replace("../../", "https://openaccess.thecvf.com/")
        pdfs += pdf

        abstract = tree_link.xpath('/html/body/div/dl/dd/div[@id="abstract"]/text()')
        abstract[0] = abstract[0].strip()
        abstracts += abstract

        author = tree_link.xpath('/html/body/div/dl/dd/div/b/i/text()')
        authors += author

        # print(title)
        # print(author)
        # print(pdf)
        # print(abstract)

        save(db, title[0], author[0], abstract[0], href, keyword)

    print(titles)
    print(hrefs)
    print(authors)
    print(abstracts)
    print(pdfs)


def save(db, title, author, abstract, link, keyword):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO papers(title, authors, abstract_text, original_link, keywords) VALUES ('%s', '%s',  '%s',  '%s', '%s')" % (title, author, abstract, link, keyword)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def save_keywords(db, keyword):
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO keywords(keyword) VALUES ('%s')" % (keyword)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    # 关闭数据库连接
    db.close()


def checkword(word):
    invalid_words = ['the', 'a', 'an', 'and', 'by', 'of', 'in', 'on', 'is', 'to', "as", "from", "for", "with", "that",
                     "have", "by", "on", "upon", "about", "above", "across", "among", "ahead", "after", "a",
                     "analthough", "at", "also", "along", "around", "always", "away", "anyup", "under", "untilbefore",
                     "between", "beyond", "behind", "because", "what", "when", "would", "could", "who", "whom", "whose",
                     "which", "where", "why", "without", "whether", "down", "during", "despite", "over", "off", "only",
                     "other", "out", "than", "the", "thenthrough", "throughout", "that", "these", "this", "those",
                     "there", "therefore", "some", "such", "since", "so", "can", "many", "much", "more", "may", "might",
                     "must", "ever", "even", "every", "each", "with", "A", "With", "From"]
    if word.lower() in invalid_words:
        return False
    else:
        return True


if __name__ == '__main__':
    getdata("https://openaccess.thecvf.com/CVPR2018?day=2018-06-19")
    getdata("https://openaccess.thecvf.com/CVPR2018?day=2018-06-20")
    getdata("https://openaccess.thecvf.com/CVPR2018?day=2018-06-21")
    getdata("https://openaccess.thecvf.com/CVPR2019?day=2019-06-18")
    getdata("https://openaccess.thecvf.com/CVPR2019?day=2019-06-19")
    getdata("https://openaccess.thecvf.com/CVPR2019?day=2019-06-20")
    getdata("https://openaccess.thecvf.com/CVPR2020?day=2020-06-16")
    getdata("https://openaccess.thecvf.com/CVPR2020?day=2020-06-17")
    getdata("https://openaccess.thecvf.com/CVPR2020?day=2020-06-18")
