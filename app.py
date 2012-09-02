from flask import Flask, url_for, request
from login import display_login_form, process_login_form

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	return "This will be the front page of SpiderSilk"


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

	return "This is the login page." 

@app.route("/register/")
def register():
	return "This is the registration page."



if __name__ == '__main__':
	app.run()


