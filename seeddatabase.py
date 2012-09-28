
# This script is a metascript.  It creates another program
# that can be executed to fill our database solidly

# first, create 10 * 10 * 10 usernames

# Then , create 20000 lorem ipsum 5 paragraph stories, with one paragraph titles
# randomly assign those stories to any of the 1000 names.

# all users will have the password "changeme"
# which looks like this:
# $2a$12$/xOeN.4B6wQsen5TgvOAMOUVvETJ8vDC8WqhjHRF2OYGSslxMmB2O


if __name__ == '__main__':
	password = '$2a$12$/xOeN.4B6wQsen5TgvOAMOUVvETJ8vDC8WqhjHRF2OYGSslxMmB2O'

	from db import User, Story, addDefault, refresh_db, session as dbsession
	import random
	import loremipsum

	for adduser in range(1,1000):
		username = "User%s" % (adduser)
		user = User(username,'',password)
		user.species = 'Automatic'
		user.bio = 'Automatic bio'
		user.email = 'Automatic@email.com'
		user.minorflag = True
		user.accepttos =True
		dbsession.add(user)
		dbsession.commit()

	for addstories in range(1,20000):
		newstory = Story(loremipsum.generate_sentence()[2])
		newstory.text = loremipsum.generate_paragraph()[2]
		newstory.adult = True
		newstory.uid = random.randrange(1000)+1
		dbsession.add(newstory)
		dbsession.commit()



