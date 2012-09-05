from flask import render_template, request, session, redirect, url_for, flash
from db import User, session as dbsession

def process_login_form():
	login = request.form['login']
	password = request.form['password']
	text = "Hello %s, your password is %s" % (login,password)
	user = dbsession.query(User).filter_by(name=login).first()
	if password == None:
		flash("Please enter a password")
		return redirect(url_for('login'))

	if user == None:
		flash("Please enter a username")
		return redirect(url_for('login'))
	
	if password == user.password:
		session['username'] = request.form['login']
	else: 
		flash("Invalid login")
		return redirect(url_for('login'))


	return redirect(url_for('hello')) 

def display_login_form():
	return render_template('login.html')

