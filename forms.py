from flask.ext.wtf import Form, TextField, PasswordField, Required, EqualTo, validators

class LoginForm(Form):
	username = TextField('Username', [Required()])
	password = PasswordField('Password', [Required()])

class RegistrationForm(Form):
	''' Let's do a basic registration form for now '''
	username = TextField('Username', [Required()])
	password = PasswordField('Password', [Required(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')


	
