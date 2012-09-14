from flask.ext.wtf import Form, TextField, PasswordField, Required, validators

class LoginForm(Form):
	username = TextField('Username', [validators.required()])
	password = PasswordField('Password', [validators.required()])
