from flask import Flask,render_template,request,redirect,url_for,session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)
app.secret_key='SecKey'
socketio = SocketIO(app)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='butterscotch'
app.config['MYSQL_DB']='gkm'

mysql=MySQL(app)

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            msg='Logged in successfully!'
            return render_template('homepage.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('userlogin.html',msg=msg)

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            msg='Logged in successfully!'
            return render_template('adminpage.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('adminlogin.html',msg=msg)

@app.route('/requests',methods=['POST','GET'])
def requests():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM accounts")
    result = cur.fetchall()
    if result:
        return render_template('requests.html',detail=result)
    else:
        return render_template('requests.html',msg='No Users Found')

@app.route('/newsofficer',methods=['POST','GET'])
def newsofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM news WHERE about=%s",("Officer",))
    result = cur.fetchall()
    if result:
        return render_template('newsofficer.html',detail=result)
    else:
        return render_template('newsofficer.html',msg='No News Found')

@app.route('/newsjco',methods=['POST','GET'])
def newsjco():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM news WHERE about=%s",("JCO/OR",))
    result = cur.fetchall()
    if result:
        return render_template('newsjco.html',detail=result)
    else:
        return render_template('newsjco.html',msg='No News Found')

@app.route('/notifofficer',methods=['POST','GET'])
def notifofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM notifications WHERE about=%s",("Officer",))
    result = cur.fetchall()
    if result:
        return render_template('notifofficer.html',detail=result)
    else:
        return render_template('notifofficer.html',msg='No Notifications Found')

@app.route('/notifjco',methods=['POST','GET'])
def notifjco():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM notifications WHERE about=%s",("JCO/OR",))
    result = cur.fetchall()
    if result:
        return render_template('notifjco.html',detail=result)
    else:
        return render_template('notifjco.html',msg='No Notifications Found')

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('main'))

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'category' in request.form and 'name' in request.form:
        username=request.form['username']
        password=request.form['password']
        mobno=request.form['mobno']
        category=request.form['category']
        gender=request.form['gender']
        name=request.form['name']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s',(username,))
        account=cursor.fetchone()
        if account:
            msg='Account already exists!'
        elif not username or not password or not category or not name:
            msg='Please Fill The form!'
        else:
            cursor.execute('INSERT INTO accounts(username,password,mobno,category,gender,name,email) VALUES(%s,%s,%s,%s,%s,%s,%s)',(username,password,mobno,category,gender,name,email,))
            mysql.connection.commit()
            msg='You Have Successfully Registered!'
    elif request.method=='POST':
        msg='Please Fill The form!'
    return render_template('register.html',msg=msg)

@app.route('/aboutarmy')
def aboutarmy():
    return render_template('about_army.html')

@app.route('/lifeinarmy')
def lifeinarmy():
    return render_template('life_in_army.html')

@app.route('/imagegallery')
def imagegallery():
    return render_template('image gallery.html')

@app.route('/videogallery')
def videogallery():
    return render_template('video_gallery.html')

@app.route('/awards')
def awards():
    return render_template('awards.html')

@app.route('/imagesports')
def imagesports():
    return render_template('image_sports.html')

@app.route('/imageevents')
def imageevents():
    return render_template('image_events.html')

@app.route('/armyinaction')
def armyinaction():
    return render_template('image_armyinaction.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/search')
def search():
    msg=''
    return render_template('search.html',msg=msg)

@app.route('/searchjobs')
def searchjobs():
    return render_template('searchjobs.html')

@app.route('/searchusername',methods=['POST','GET'])
def searchusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE username like %s",(username1,))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('fetch.html',detail=result)
            else:
                return render_template('fetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('fetch.html',msg=msg)

@app.route('/adminsearchusername',methods=['POST','GET'])
def adminsearchusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE username like %s",(username1,))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('adminfetch.html',detail=result)
            else:
                return render_template('adminfetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('adminfetch.html',msg=msg)

@app.route('/searchname',methods=['POST','GET'])
def searchname():
    msg=''
    if request.method=='POST' and 'name' in request.form:
        name=request.form['name']
        name1="%"+name+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE name like %s",(name1,))
        result=cur.fetchall()
        if not name:
            msg='Please Enter Name to Search'
        else:
            if result:
                return render_template('fetch.html',detail=result)
            else:
                return render_template('fetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Name to Search'
    return render_template('fetch.html',msg=msg)

@app.route('/adminsearchname',methods=['POST','GET'])
def adminsearchname():
    msg=''
    if request.method=='POST' and 'name' in request.form:
        name=request.form['name']
        name1="%"+name+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE name like %s",(name1,))
        result=cur.fetchall()
        if not name:
            msg='Please Enter Name to Search'
        else:
            if result:
                return render_template('adminfetch.html',detail=result)
            else:
                return render_template('adminfetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Name to Search'
    return render_template('adminfetch.html',msg=msg)

@app.route('/fetchuser',methods=['POST','GET'])
def fetchuser():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts")
    result=cur.fetchall()
    if result:
        return render_template('adminfetch.html',detail=result)
    else:
        return render_template('adminfetch.html',msg='No Users Found')

@app.route('/fetchcivilian',methods=['POST','GET'])
def fetchcivilian():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE category=%s",("Civilian",))
    result=cur.fetchall()
    if result:
        return render_template('fetch.html',detail=result)
    else:
        return render_template('fetch.html',msg='No Users Found')

@app.route('/fetchofficer',methods=['POST','GET'])
def fetchofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE category=%s",("Officer",))
    result=cur.fetchall()
    if result:
        return render_template('fetch.html',detail=result)
    else:
        return render_template('fetch.html',msg='No Users Found')

@app.route('/eligibility',methods=['GET','POST'])
def eligibility():
    msg=''
    if request.method=='POST' and 'age' in request.form and 'gender' in request.form and 'qualification' in request.form:
        age=request.form['age']
        gender=request.form['gender']
        qualification=request.form['qualification']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT title FROM jobs WHERE minage<=%s and maxage>=%s and gender=%s and qualification=%s",(age,age,gender,qualification,))
        result=cur.fetchall()
        if result:
            return render_template('eligibility.html',detail=result)
        else:
            return render_template('eligibility.html',msg='No Users Found')

@app.route('/deleteacc/<string:id>',methods=['POST','GET'])
def deleteacc(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM accounts WHERE username=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('adminfetch.html',msg='Account Deleted Successfully')

@app.route('/deleteuser')
def deleteuser():
    return render_template('deleteuser.html')

@app.route('/addnews',methods=['GET','POST'])
def addnews():
    msg=''
    if request.method=='POST' and 'newsid' in request.form and 'title' in request.form and 'link' in request.form and 'about' in request.form:
        newsid=request.form['newsid']
        title=request.form['title']
        link=request.form['link']
        about=request.form['about']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM news WHERE newsid=%s',(newsid,))
        account=cursor.fetchone()
        if account:
            msg='NewsID already exists!'
        elif not newsid or not title or not link or not about:
            msg='Please Fill The Fields!'
        else:
            cursor.execute('INSERT INTO news VALUES(%s,%s,%s,%s)',(newsid,title,link,about,))
            mysql.connection.commit()
            msg='Entry Added Successfully!'
    elif request.method=='POST':
        msg='Please Fill The Fields!'
    return render_template('addnews.html',msg=msg)

@app.route('/addnotif',methods=['GET','POST'])
def addnotif():
    msg=''
    if request.method=='POST' and 'notifid' in request.form and 'title' in request.form and 'link' in request.form and 'about' in request.form:
        notifid=request.form['notifid']
        title=request.form['title']
        link=request.form['link']
        about=request.form['about']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM notifications WHERE notifid=%s',(notifid,))
        account=cursor.fetchone()
        if account:
            msg='NotifID already exists!'
        elif not notifid or not title or not link or not about:
            msg='Please Fill The Fields!'
        else:
            cursor.execute('INSERT INTO notifications VALUES(%s,%s,%s,%s)',(notifid,title,link,about,))
            mysql.connection.commit()
            msg='Entry Added Successfully!'
    elif request.method=='POST':
        msg='Please Fill The Fields!'
    return render_template('addnotif.html',msg=msg)

@app.route('/sessions')
def sessions(methods=['GET', 'POST']):
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == "__main__":
    socketio.run(app, debug=True)
