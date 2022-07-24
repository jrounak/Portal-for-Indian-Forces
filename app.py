from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)
app.secret_key='SecKey'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='butterscotch'
app.config['MYSQL_DB']='gkm'

mysql=MySQL(app)

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
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
            return render_template('index.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('login.html',msg=msg)
@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('login'))
@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'mobno' in request.form:
        username=request.form['username']
        password=request.form['password']
        mobno=request.form['mobno']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s',(username,))
        account=cursor.fetchone()
        if account:
            msg='Account already exists!'
        elif not username or not password or not mobno:
            msg='Please fill the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES(%s,%s,%s)',(username,password,mobno,))
            mysql.connection.commit()
            msg='You have successfully registered!'
    elif request.method=='POST':
        msg='Please fill the form!'
    return render_template('register.html',msg=msg)

if __name__=="__main__":
    app.run(debug=True)
