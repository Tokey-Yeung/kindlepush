from flask import Flask,render_template
from faker import Faker
import random
import datetime


app=Flask(__name__)



def before():
    fake = Faker('zh_CN')
    name = fake.name()
    name2 = fake.name()
    phone_num = fake.phone_number()
    student_code = "189054" + str(random.randint(110, 200))
    start_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
    end_time = (datetime.datetime.now() + datetime.timedelta(days=2)+ datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
    ok_time = (datetime.datetime.now()+ datetime.timedelta(hours=8)).strftime("%Y-%m-%d")
    return name,name2,phone_num,student_code,start_time,end_time,ok_time

@app.route("/hi")
def updata():
    return '<h1>Hello，{}</h1>'.format((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/')
def fake():
    name, name2, phone_num, student_code, start_time, end_time, ok_time = before()
    return render_template("fake.html",name=name,name2=name2,phone=phone_num,student_code=student_code,start_time=start_time,end_time=end_time,ok_time=ok_time)

if __name__ == '__main__':
    app.run()