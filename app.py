from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia

api = os.getenv("makersuite")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

app = Flask(__name__)

flag = 1

@app.route("/", methods=["POST", "GET"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods=['GET', 'POST'])
def main():
    global flag
    if flag == 1:
        t = datetime.datetime.now()
        user_name = request.form.get("q")
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?,?)", (user_name, t))
        conn.commit()
        c.close()
        conn.close
        flag = 0
    return(render_template("main.html"))

@app.route("/foodexp", methods=['GET', 'POST'])
def foodexp():
    return(render_template("foodexp.html"))

@app.route("/foodexp1", methods=['GET', 'POST'])
def foodexp1():
    return(render_template("foodexp1.html"))

@app.route("/foodexp2", methods=['GET', 'POST'])
def foodexp2():
    return(render_template("foodexp2.html"))

@app.route("/foodexp_pred", methods=['GET', 'POST'])
def foodexp_pred():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html", r=(q*0.4851)+147.4))

@app.route("/ethical_test", methods=['GET', 'POST'])
def ethical_test():
    return(render_template("ethical_test.html"))

@app.route("/test_result", methods=['GET', 'POST'])
def test_result():
    answer = request.form.get("answer")
    if answer =="false":
        return(render_template("pass.html"))
    elif answer =="true":
        return(render_template("fail.html"))

@app.route("/FAQ", methods=['GET', 'POST'])
def FAQ():
    return(render_template("FAQ.html"))

@app.route("/FAQ1", methods=['GET', 'POST'])
def FAQ1():
    r = model.generate_content("Factors for Profit")
    return(render_template("FAQ1.html", r=r.candidates[0].content.parts[0]))

@app.route("/FAQinput", methods=['GET', 'POST'])
def FAQinput():
    q = request.form.get("q")
    r = wikipedia.summary(q)
    return(render_template("FAQinput.html", r=r))

@app.route("/userLog", methods=['GET', 'POST'])
def userLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
        r = r + str(row) + "\n"
    print(r)
    c.close()
    conn.close
    return(render_template("userLog.html", r=r))   

@app.route("/deleteLog", methods=['GET', 'POST'])
def deleteLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close
    return(render_template("deleteLog.html"))

if __name__ == "__main__":
    app.run()
