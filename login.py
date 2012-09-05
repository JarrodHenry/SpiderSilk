from flask import render_template, request, session, redirect, url_for, flash
from db import User, session as dbsession

def process_login_form():
	login = request.form['login']
	password = request.form['password']
	text = "Hello %s, your password is %s" % (login,password)
	user = dbsession.query(User).filter_by(name=login).first()
	
	if password == user.password:
		session['username'] = request.form['login']
		flash("Login Successful")	
	else: 
		flash("Invalid login")

	return redirect(url_for('hello')) 

def display_login_form():
	flash ("User Logged Out")

	return render_template('login.html')

