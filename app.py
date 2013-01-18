from flask import Flask, url_for, request, session, redirect, render_template, flash
from forms import LoginForm, RegistrationForm, StoryForm
from db import User, Story, Tag, Reccomendation, session as dbsession
from datetime import datetime
from flask.ext.bcrypt import Bcrypt
import markdown

app = Flask(__name__)
app.debug = True

#### CHANGE THIS BEFORE DEPLOYMENT
app.secret_key = 'xf9xfeGxa1axa8xfb8dxe2xd2bWxeaxb71x0efei'
###################################
#
# TODO: Factor this out in deployment/install milestone
#

bcrypt = Bcrypt(app)


@app.route("/")
def hello():
    if 'username' in session:
        user = session['username']
    else:
        user = None

    # Get the list of users on the site
    #userlist = dbsession.query(User.name).order_by(User.id.desc()).limit(30)
    storylist = dbsession.query(Story.title, Story.id).order_by(Story.id.desc()).limit(30)
    return render_template('frontpage.html', user=user, storylist=storylist)


@app.route("/story/new", methods=['GET', 'POST'])
def storynew():
    if 'username' in session:
        user = session['username']
        form = StoryForm()
        if form.validate_on_submit():
            uid = dbsession.query(User.id).filter_by(name=user).first()
            newstory = Story(form.title.data)
            newstory.text = markdown.markdown(form.body.data)
            newstory.uid = uid[0]
            newstory.adult = form.adult.data
            tagslist = form.tags.data
            tagslist = tagslist.split(',')

            for tagitem in tagslist:
                tagitem = tagitem.strip()
                tagitem = tagitem.lower()

                tag = dbsession.query(Tag).filter_by(tagname=tagitem).first()
                if tag is None:
                    tag = Tag(tagitem)

                newstory.tags.append(tag)
            dbsession.add(newstory)
            dbsession.commit()
            return redirect("~" + user)
        return render_template("storynew.html", form=form)
    else:
        return render_template("storynew.html")


@app.route("/story/<int:story_id>", methods=['GET', 'POST'])
def story(story_id):
    user = None
    if 'username' in session:
        user = session['username']

    if request.method == 'GET':
        story = dbsession.query(Story).filter_by(id=story_id).first()
        if story is None:
            flash("Story does not exist!")
            return redirect(url_for('hello'))
        else:
            return render_template('story.html', story=story, user=user)
    elif request.method == 'POST':
        if user == request.form['user']:
            story = dbsession.query(Story).filter_by(id=story_id).first()
            dbsession.delete(story)
            dbsession.commit()
        else:
            flash("Cannot delete story without permission")

        return redirect(url_for('hello'))


@app.route("/story/fave/<int:story_id>", methods=['GET', 'POST'])
def favestory(story_id):
    user = None
    if 'username' in session:
        if request.method == 'POST':
            user = session['username']
            u = dbsession.query(User).filter_by(name=user).first()
            s = dbsession.query(Story).filter_by(id=story_id).first()
            u.faves.append(s)
            dbsession.add(u)
            dbsession.commit()
            flash("Fave'd story ")
    return redirect('/story/' + str(story_id))


@app.route("/story/rec/<int:story_id>", methods=['GET', 'POST'])
def recstory(story_id):
    if 'username' in session:
        if request.method == 'POST':
            user = session['username']

            s = dbsession.query(Story).filter_by(id=story_id).first()
            u = dbsession.query(User).filter_by(name=user).first()

            comment = request.form['comment']
            rec = Reccomendation(comment)
            rec.uname = user
            rec.uid = u.id
            rec.sid = story_id
            rec.date = datetime.now()

            s.recs.append(rec)
            dbsession.add(s)
            dbsession.commit()
    return redirect('/story/' + str(story_id))


@app.route("/~<user_name>")
@app.route("/user/<user_name>")
def user(user_name):
    user = dbsession.query(User).filter_by(name=user_name).first()
    if user is None:
        flash("User not found")
        return redirect(url_for('hello'))
    else:
        return render_template('user.html', user=user)


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
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
        session.pop('username', None)
    return redirect(url_for('hello'))


@app.route("/register/", methods=['GET', 'POST'])
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


@app.route("/tag/<tag_id>")
def tagload(tag_id):
    storylist = dbsession.query(Story).filter(Story.tags.any(Tag.id == tag_id)).all()
    if storylist is None:
        flash("No stories with this tag found")
        return redirect(url_for('hello'))
    else:
        return render_template("tag.html", storylist=storylist)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        flash("Please use the search box to search")
        return redirect(url_for('hello'))

    term = request.form['searchitem']
    storylist = dbsession.query(Story).filter(Story.text.contains(term)).all()
    storylist[1:1] = dbsession.query(Story).filter(Story.title.contains(term)).all()
    storytagged = dbsession.query(Story).filter(Story.tags.any(Tag.tagname == term)).all()
    return render_template("search.html", storytagged=storytagged, term=term, storylist=storylist)


@app.route('/user/follow/<user_id>', methods=['POST'])
def followUser(user_id):
    return "User %s followed by user %s." % (user_id, session['username'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
