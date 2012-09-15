from flask import Flask, url_for, request, session, redirect, render_template,flash
from forms import LoginForm, RegistrationForm
from db import User, refresh_db, addDefault, session as dbsession

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
	form = LoginForm()

	if  form.validate_on_submit():
		login = form.username.data
		password = form.password.data
		user = dbsession.query(User).filter_by(name=login).first()
		
		if user is None:
			flash("No such user")
			return redirect(url_for('login'))

		if bcrypt.check_password_hash(user.password, password):
			session['username'] = login
			return redirect(url_for('hello'))
		else:
			flash("Invalid login")
			return redirect(url_for('login'))
	else:
		return render_template('login.html', form=form)	

@app.route("/logout/")
def logout():
	if 'username' in session:
		session.pop('username',None)
	return redirect(url_for('hello'))

@app.route("/register/", methods=['GET','POST'])
def register():
	if 'username' in session:
		flash("Cannot create new account while logged in.")
		return redirect(url_for('hello'))
	else:	
		form = RegistrationForm()
	
		if form.validate_on_submit():
			login = form.username.data
			user = dbsession.query(User).filter_by(name=login).first()
		
			if user is None:
				pw_hash = bcrypt.generate_password_hash(form.password.data)
				user = User(login, '', pw_hash)
				user.gender = form.gender.data
				user.species = form.species.data
				user.bio = form.bio.data
				user.email = form.email.data
				user.minorflag = not form.adult.data
				user.accepttos = True
				
				dbsession.add(user)
				dbsession.commit()

				flash("User Created")
				return redirect(url_for('login'))
			else:
				flash("User already exists.")
				return redirect(url_for('register'))
		
	return render_template('register.html', form=form)

@app.route("/resetdb/", methods = ['GET', 'POST'])
def resetdb():
	if request.method=='POST':
		refresh_db()
		addDefault()
		flash('Database Reset -  Please remove this function prior to deployment')
		return redirect(url_for('hello'))
	else:
		return render_template('resetdb.html')


if __name__ == '__main__':
	app.run()


