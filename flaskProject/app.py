from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
import re
from Search import qishu_search,caimoge_search


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


def craw(way,keywords):         #根据选择的书源来源不同来选择从不同的站获取数据
    if way=='way1':         #获取源为采墨阁
        content,res_html=caimoge_search(keywords)
        source='采墨阁'
    elif way=='way2':    #获取源为奇书kankezw
        content,res_html=qishu_search(keywords)
        source='奇书网'
    return content,res_html,source



@app.route('/')             #主页路由
def index():
    motto=get_motto()
    return render_template("index.html",**locals())            #返回首页

@app.route("/search",methods=['POST'])              #搜索请求
def postdata():
    result = request.form
    #判断搜索关键字
    if len(result.get('keyword',''))!=0:
        keywords = result["keyword"]
    else:
        if len(result['author']) == 0:
            keywords = result["bookname"]
        elif len(result['bookname']) == 0:
            keywords = result["author"]
        else:
            keywords = result["bookname"]
    contents,res_html,source=craw(way=result['approach'],keywords=keywords)
    return render_template(res_html,**locals())




if __name__ == '__main__':
    app.run(debug = True)
