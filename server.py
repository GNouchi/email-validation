from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re 
app = Flask(__name__)
app.secret_key = "C3190FB0A2279EF8DA84CB4C577BED27398CDBD30A72D94E77647506B9739ED0"
mysql = connectToMySQL('friendsdb')
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

@app.route('/')
def landing():
    userdata = mysql.query_db("Select * from userdata")
    color = ''
    if '_flashes' in session:
        color = session['_flashes'][0][0]
    return render_template("index.html", userdata = userdata,color=color)

@app.route("/validate" , methods = ["POST"])
def vvvv():
    # print(request.form['email'])
    # print(EMAIL_REGEX.match(request.form['email']))
    if 'win' not in session:
        session['win'] = 0 
    else:
        session['win'] = 0
    if request.form['email']=='':
        flash(u'Can you...like...type something?','#d84444')
        session['win'] = 1 
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Sorry, we can only accept english-based emails", '#d84444')
        session['win'] = 1 

#query only if all other checks pass
    userdata = mysql.query_db("Select * from userdata")
    for x in userdata:
        if x['email'] == request.form['email']:
            flash("Not saying it exists...but also not saying it doesn't exist.",'#d84444' )
            session['win'] = 1 
# THE CULLING
    if session['win'] == 1:
        return redirect ('/')
# LET WINNERS THROUGH
    if session['win']== 0:
        flash("Here's your treasure!", '#63ff3d')
        query = "INSERT INTO userdata (email, create_d, update_d) VALUES (%(email)s, NOW(), NOW());"
        data = {'email' : request.form['email']}
        x = mysql.query_db(query, data)
        return redirect ('success')
# fallback
    return redirect ('/')

@app.route('/success', methods = ['POST', 'GET'])
def backhome():
# home redirect
    if request.method =="POST" and 'home' in request.form:
        return redirect ('/')

# removal logic
    userdata = mysql.query_db("Select * from userdata")
    if request.method == "POST":
        for i in request.form:
            data = {'id' : request.form[i]}
            print("************************")
            query = "DELETE FROM userdata WHERE id = %(id)s ;"            
            x = mysql.query_db(query, data)
            return redirect('/success')
# success page color assignment
    color = ''
    if '_flashes' in session:
        color = session['_flashes'][0][0]
    return render_template("success.html", userdata = userdata,color=color)

if __name__ == "__main__":
    app.run(debug = True)