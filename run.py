from  flask import Flask,render_template
from  flask_sqlalchemy import SQLAlchemy
from datetime  import datetime
app=Flask(__name__)
app.debug=True
#app的配置以中括号的形式指定一个键值
#SQLALCHEMY_DATABASE_URI（固定写法）译：sqlalchemy所使用的数据库的统一资源定位器，俗称数据库地址
#?check_same_thread=False解决多线程问题
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///./db/test.db"
#在控制台可以跟踪改变,不加在控制台报警告
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
db=SQLAlchemy(app)#创建数据库的核心对象，并绑定app对象建立关系
#db.init_app(app)#db初始化绑定app对象（绑定方法2）缺陷：控制台测试没有执行时机

#继承自基类db.model，原因：db.Model后台做了一些完成和数据库关联的关键操作
class User(db.Model):
    #通过源数据的方式指定表名，不指定默认类名
    __tablename__="user"
    #写的类的字段相当于表的字段
    #db.column使用db实例生成一个数据库的列
    #db.Integer数据库中这个列是整型的
    id =db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(100))
    created_time=db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,email,password,created_time=datetime.now()):
        self.username=username
        self.email=email
        self.password=password
        self.created_time=created_time
    def __repr__(self):
        return "<用户名：{id},{username},{email}>".format(id=self.id,username=self.username,email=self.email)
@app.route("/")
def index():
    return "helloword"

@app.route("/db/")
def initialize_db():
    db.create_all()
    return "OK"

@app.route("/user/")
def user_list():
    users=db.session.query(User).all()
    return render_template("user_list.html",users=users)
    #return "{}".format(users[0])

if __name__=="__main__":
    app.run()