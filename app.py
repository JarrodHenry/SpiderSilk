from flask import Flask, url_for, request, session, redirect, render_template
from login import display_login_form, process_login_form
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.debug = True
app.secret_key = 'xf9xfeGxa1axa8xfb8dxe2xd2bWxeaxb71x0efei'
bcrypt = Bcrypt(app)

 

@app.route("/")
def hello():
	
	if 'username' in session:
		user = session['username']
	else: 
		user = None

	return render_template('frontpage.html', user=user) 


@app.route("/story/<int:story_id>")
def story(story_id):
	return "You have selected story %s" % story_id

@app.route("/user/<user_name>")
def user(user_name):
	return "You have selected user %s " % user_name

@app.route("/login/", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return process_login_form()	
	else:
		return display_login_form()	

@app.route("/logout/")
def logout():
	if 'username' in session:
		session.pop('username',None)

	return redirect(url_for('hello'))



@app.route("/register/")
def register():
	return "This is the registration page."



if __name__ == '__main__':
	app.run()


