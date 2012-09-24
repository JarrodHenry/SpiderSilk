from flask.ext.wtf import Form, TextField, PasswordField, Required, EqualTo, validators, TextAreaField, BooleanField

class LoginForm(Form):
	username = TextField('Username', [Required()])
	password = PasswordField('Password', [Required()])

class RegistrationForm(Form):
	''' Let's do a basic registration form for now '''
	username = TextField('Username', [Required()])
	password = PasswordField('Password', [Required(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	species = TextField('Species')
	gender = TextField('Gender') 
	email = TextField('Email address', [Required(), validators.Email()])
	bio = TextAreaField('Bio')
	adult = BooleanField('I am an adult.')
	accepttos = BooleanField('I accept the terms of service.', [validators.Required( message='You must accept the terms of service')])

class StoryForm(Form):
	''' This will allow users to add stories '''
	title = TextField('Title', [Required()])
	body = TextAreaField("Body", [Required()])
	adult = BooleanField("Adult Topics")

	
