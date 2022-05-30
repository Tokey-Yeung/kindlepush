import requests
import time
from bs4 import BeautifulSoup

def res():
   while True:
       r = requests.get("http://mse.ustb.edu.cn/xueyuangonggao")
       r.encoding = "UTF-8"
       soup = BeautifulSoup(r.text, "html.parser")
       soup = soup.find_all(class_="ky")[0].find_all('li')[0]
       text = soup.get_text()
       url = soup.find_all("a")[0].get("href")
       if text == "北京科技大学材料学部2022年硕士研究生复试时间安排[2022-03-25]":
           print("还没有发布")
           time.sleep(60)
       else:
           print("已发布，正在通知")
           requests.post("https://qmsg.zendee.cn:443/send/9054782835afc6e92567ddd260639f41",
                         data={"msg": "复试成绩已出，请查看\n{}".format(text)})
           break


if __name__ == '__main__':
    res()