from datetime import timedelta
import os
from flask import Flask, render_template, request, redirect, session,flash
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime= timedelta(minutes=5)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        session.permanent=True
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        # wrong way
        # cur.execute("SELECT * FROM admin WHERE email = '"+ email +"' AND password = '"+ password +"' ;")
        # correct way
        # Validate input data
        # if not email or not password:
        #   return render_template('error.html', message='email and password are required.')

        # if len(email) > 50 or len(password) > 50:
        #   return render_template('error.html', message='email and password must be less than 50 characters.')

        # # if not email.isalnum() or not password.isalnum():
        # #   return render_template('error.html', message='email and password can only contain alphanumeric characters.')
        query = "SELECT * FROM admin WHERE email=? AND password=?"
        cur.execute(query, (email, password))
        user = cur.fetchone()
        conn.commit()

        if user:
            # Store the user's ID in the session
            session['user_id'] = user[0]
            return redirect('/home')
        else:
            return render_template('error.html')

    # Always render the login template, even if the user is already logged in
    if 'user_id' in session:
        return redirect('/home')
    return render_template('login.html')


@app.route('/home')
def home():
    # Redirect to the login page if the user is not logged in
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('homep.html')


@app.route('/create', methods=["GET", "POST"])
def create():
    # Redirect to the login page if the user is not logged in
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('create.html')


@app.route('/logout')
def logout():
    
    # Clear the user's session
    session.pop('user_id', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
