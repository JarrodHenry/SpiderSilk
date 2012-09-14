from flask import render_template, request, session, redirect, url_for, flash
from db import User, session as dbsession
#from wtforms import Form, PasswordField, TextField, validators
from flask.ext.wtf import Form, TextField, PasswordField, Required, validators

class LoginForm(Form):
	username = TextField('Username', [validators.required()])
	password = PasswordField('Password', [validators.required()])
