from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_motto():#获取格言
    try:
        url = "https://v2.alapi.cn/api/shici"
        payload = "token=AzOZNtBaJAgKgByI&format=json&type=all"
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        resjs=response.json()
        if resjs['msg']=='success':
            motto=resjs['data']['content']+'——'+resjs['data']['author']+'《{}》'.format(resjs['data']['origin'])
        else:
            r = requests.get('https://api.ghser.com/qinghua/', headers=headers)
            motto = r.text
    except:
        r = requests.get('https://api.ghser.com/qinghua/',headers=headers)
        motto = r.text
    return motto



def caimoge(keywords):
    content = []
    res = requests.post("https://www.caimoge.net/search", data={"searchkey": keywords})
    if res.status_code == 200:
        html = res.text.replace("状态：", "$%").replace("小类：", "$%").replace("字数：", "$%").replace("作者：", "$%").replace(
            "更新时间：", "$%")
        soup = BeautifulSoup(html, "html.parser")
        book_list = soup.find_all("dl")
        if len(book_list) == 0:
            pass
        else:
            for i in range(0, len(book_list)):
                bookitems = {
                    'bookname': '',
                    'bookid': '',
                    'book_author': '',
                    'book_des': '',
                    'book_status': '',
                    'booktype': '',
                    'wordcounts': '',
                    'booktime': '',
                    'new_char': '',
                    'new_url': '',
                    'pic_id': '',
                }
                bookid = book_list[i].h3.find("a")["href"]
                if re.search("[1-9][0-9]{2,}", bookid) == None:
                    bookitems['bookid'] = re.search("[0-9]", bookid).group(0)
                else:
                    bookitems['bookid'] = re.search("[1-9][0-9]{2,}", bookid).group(0)
                    bookitems['bookname'] = book_list[i].find_all("h3")[0].find_all('a')[0].get_text()
                    book_other = book_list[i].find_all(class_="book_other")
                    bookitems['book_author'] = book_other[0].get_text().split('$%')[1]
                    bookitems['book_des'] = book_list[i].find(class_="book_des").get_text()
                    bookitems['book_status'] = book_other[0].get_text().split('$%')[2]
                    bookitems['booktype'] = book_other[0].get_text().split('$%')[3]
                    bookitems['wordcounts'] = book_other[0].get_text().split('$%')[4]
                    bookitems['booktime'] = book_other[1].get_text().split('$%')[1]
                    bookitems['new_char'] = book_other[1].find_all('a')[0].get_text()
                    bookitems['new_url'] = book_other[1].find_all('a')[0]['href']
                if len(bookitems['bookid']) > 4:
                    pic_id = bookitems['bookid'][0:2]
                elif len(bookitems['bookid']) <= 3:
                    pic_id = "0"
                else:
                    pic_id = bookitems['bookid'][0]
                bookitems['pic_url']='http://img.caimoge.net/{}/{}/{}s.jpg'.format(pic_id,bookitems['bookid'],bookitems['bookid'])

                content.append(bookitems)  # 将采集到的书籍信息添加到列表，返回给前端
                res_html="result.html"              #数据正常的话就返回结果页
    else:
        msg = "云端数据库-采墨阁-连接错误，无法查询你要下载的书籍，请稍后再试"
        res_html = "404.html"
    return content,res_html

#通过页面的<tr>标签获取书籍信息
def qishu(keywords):
    content = []
    res = requests.get("https://www.kankezw.com/search.html?searchkey={}" .format(keywords))
    if res.status_code == 200:
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        book_list = soup.find_all("tr")
        #遍历book_list，获取书籍信息
        if len(book_list) == 0:
            pass
        else:
            for i in range(0,len(book_list)):
                bookitems = {
                    'bookname': '',
                    'bookid': '',
                    'book_author': '',
                    'book_des': '',
                    'book_status': '',
                    'booktype': '',
                    'wordcounts': '',
                    'booktime': '',
                    'new_char': '',
                    'new_url': '',
                    'pic_url': '',
                }
    else:
        pass




def craw(way,keywords):         #根据选择的书源来源不同来选择从不同的站获取数据
    if way=='way1':         #获取源为采墨阁
        content,res_html=caimoge(keywords)
    elif way=='way2':
        pass
    return content,res_html



@app.route('/')             #主页路由
def index():
    motto=get_motto()
    return render_template("index.html",**locals())            #返回首页

@app.route("/search",methods=['POST'])              #搜索请求
def postdata():
    result = request.form
    if len(result.get('keyword',''))!=0:
        keywords = result["keyword"]
    else:
        if len(result['author']) == 0:
            keywords = result["bookname"]
        elif len(result['bookname']) == 0:
            keywords = result["author"]
        else:
            keywords = result["bookname"]
    contents,res_html=craw(way=result['approach'],keywords=keywords)
    return render_template(res_html,**locals())




if __name__ == '__main__':
    app.run(debug = True)
