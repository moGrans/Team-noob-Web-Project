from bottle import *
import os

''' This is a program testing the functionality of crawler, ignore in the finished edition '''

@route('/')
def index():
    return template("Tester.tpl")

@route('/TestFiles/<name>')
def Test(name):
    return template(os.getcwd()+"/TestFiles/" + name)


if __name__ == "__main__":
    run(reloader=True)