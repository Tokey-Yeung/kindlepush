#采用阅读的书源来获取书籍信息。
import requests
from bs4 import BeautifulSoup
import datetime
import re


def qishu_search(keywords):       #使用奇书网kankezw搜索
    content = []
    res=requests.get("https://www.kankezw.com/search.html?searchkey={}".format(keywords))
    res.encoding="utf-8"
    soup=BeautifulSoup(res.text,'html.parser')
    ls=soup.find_all('tr')          #书籍列表在tr标签中
    for i in ls[1:]:
        bookname = i.find_all('a')[0].get_text()  # 书名获取
        author = i.find_all('td')[2].get_text()  # 作者获取
        lastChapter = i.find_all('a')[1].get_text()  # 最新章节获取
        bookUrl = 'https://www.kankezw.com' + i.find_all('a')[0]['href']  # 书籍详情页Url获取
        detail_page = requests.get(bookUrl)  # 访问书籍详情页获取更多的信息，如封面等
        detail_page.encoding = 'utf-8'
        detail_soup = BeautifulSoup(detail_page.text, 'html.parser')  # 解析详情页
        booktype = detail_soup.find_all('a')[2].get_text()  # 从详情页获取书籍种类
        wordCount=detail_soup.find_all(class_='small')[1].get_text().replace('文件大小：','')  # 从详情页获取书籍字数或文件大小
        booktime = detail_soup.find_all(class_='small')[3].get_text().replace('更新日期：', '')  # 获取更新时间
        bookstatus = detail_soup.find_all(class_='small')[4].get_text().replace('连载状态：', '')  # 获取书籍状态
        intro = detail_soup.find_all(class_='showInfo')[0].p.get_text()  # 从详情页获取书籍简介
        coverUrl = "https://www.kankezw.com" + detail_soup.find_all(class_='detail_pic')[0].img.get('src')  # 获取封面Url
        downUrl = detail_soup.find_all(class_='showDown')[0].find_all('script')[0].get_text()[13:-2].split(',')[
            1]  # 获取下载地址,并以‘,’分割，将downUrl分割成一个个的url
        lastChapterUrl = "https://www.kankezw.com" + detail_soup.find_all(class_='downButton')[0]['href']  # 获取最新章节的url
        #生成空白字典bookitems,存储书籍信息,含有bookname,author,lastChapter,booktype,booktime,intro,coverUrl,downUrl
        bookitems = {'bookname': '', 'author': '', 'lastChapter': '', 'booktype': '', 'booktime': '', 'intro': '',  'coverUrl': '', 'downUrl': '','bookUrl':'','bookstatus':'','wordCount':'','lastChapterUrl':''}
        bookitems['bookname'] = bookname
        bookitems['author'] = author
        bookitems['lastChapter'] = lastChapter
        bookitems['lastChapterUrl']=bookUrl
        bookitems['booktype'] = booktype
        bookitems['booktime'] = booktime
        bookitems['bookstatus'] = bookstatus
        bookitems['intro'] = intro
        bookitems['wordCount'] = wordCount
        bookitems['coverUrl'] = coverUrl
        bookitems['downUrl'] = downUrl
        bookitems['bookUrl'] = bookUrl
        bookitems['lastChapterUrl'] = lastChapterUrl
        content.append(bookitems)
    res_html='result.html'
    return content,res_html



def caimoge_search(keywords):             #采墨阁搜索
    content = []
    pattern = re.compile('-?[1-9]\d*')            #正则表达式，用于提取数字
    res = requests.post("https://www.caimoge.net/search", data={"searchkey": keywords})
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    ls = soup.find_all('dl')
    for i in ls:
        bookname = i.h3.a.get_text()  # 书名获取
        print(bookname)
        bookother = i.find_all('dd')[1].find_all('span')
        author = bookother[0].get_text()
        bookstatus = bookother[1].get_text()  # 从详情页获取书籍种类
        booktype = bookother[2].get_text()  # 从详情页获取书籍种类
        wordCount = bookother[3].get_text() +'万' # 从详情页获取书籍字数或文件大小
        lastChapter = i.find_all('dd')[3].find_all('a')[0].get_text()  # 最新章节获取
        booktime= i.find_all('dd')[3].find_all('span')[0].get_text()  # 获取更新时间
        bookUrl = 'https://www.caimoge.net' + i.h3.a['href']  # 书籍详情页Url获取
        intro= i.find_all('dd')[2].get_text()
        coverUrl = i.find_all(class_='lazyload')[0].get('src')     # 获取封面Url
        downUrl = 'https://www.caimoge.net/api/txt_down.php?articleid={}&articlename={}'.format(pattern.search(bookUrl).group(0),bookname)  # 获取下载地址
        lastChapterUrl = 'https://www.caimoge.net' + i.find_all('dd')[3].find_all('a')[0]['href']  # 获取最新章节的url
        # 生成空白字典bookitems,存储书籍信息,含有bookname,author,lastChapter,booktype,booktime,intro,coverUrl,downUrl
        bookitems = {'bookname': '', 'author': '', 'lastChapter': '', 'booktype': '', 'booktime': '', 'intro': '',
                     'coverUrl': '', 'downUrl': '', 'bookUrl': '', 'bookstatus': '', 'wordCount': '',
                     'lastChapterUrl': ''}
        bookitems['bookname'] = bookname
        bookitems['author'] = author
        bookitems['lastChapter'] = lastChapter
        bookitems['lastChapterUrl'] = bookUrl
        bookitems['booktype'] = booktype
        bookitems['booktime'] = booktime
        bookitems['bookstatus'] = bookstatus
        bookitems['intro'] = intro
        bookitems['wordCount'] = wordCount
        bookitems['coverUrl'] = coverUrl
        bookitems['downUrl'] = downUrl
        bookitems['bookUrl'] = bookUrl
        bookitems['lastChapterUrl'] = lastChapterUrl
        content.append(bookitems)
    res_html = 'result.html'
    return content, res_html


if __name__ == '__main__':
    pass