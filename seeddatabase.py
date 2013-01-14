
# first, create 10 * 10 * 10 usernames

# Then , create 20000 lorem ipsum 5 paragraph stories, with one paragraph titles
# randomly assign those stories to any of the 1000 names.

# all users will have the password "changeme"
# which looks like this:
# $2a$12$/xOeN.4B6wQsen5TgvOAMOUVvETJ8vDC8WqhjHRF2OYGSslxMmB2O


if __name__ == '__main__':
	password = '$2a$12$/xOeN.4B6wQsen5TgvOAMOUVvETJ8vDC8WqhjHRF2OYGSslxMmB2O'

	from db import User, Story, Tag, Reccomendation, addDefault, refresh_db, session as dbsession
	import random
	import loremipsum
	from datetime import datetime

	refresh_db()
 	addDefault()
	print "Added Admin account."

	print "Adding users."

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
	print "Added users."

	print "Adding stories."
	counter = 0
	while counter < 20000:
		newstory = Story(loremipsum.generate_sentence()[2])
		newstory.text = loremipsum.generate_paragraph()[2]
		newstory.adult = True
		newstory.uid = random.randrange(999)+1
		dbsession.add(newstory)
		counter = counter + 1
	dbsession.commit()
	print "Added stories."

	print "Adding Tags."

	for tagnumber in range(1,100):
		tag = Tag("tag"+str(tagnumber))
		dbsession.add(tag)
	dbsession.commit()
	print "Added tags."

	print "Adding tags to stories"
	for stories in range(1,20000):
		story = dbsession.query(Story).filter_by(id = stories).first()
		for newtagid in range(0,5):
			tag = dbsession.query(Tag).filter_by(id = random.randrange(99)).first()
			story.tags.append(tag)
		dbsession.commit()
		if stories % 500 == 0: 
			print "Story " + str(stories) + " tagged."

	print "Adding faves"
	for user in range(1,1000):
		u = dbsession.query(User).filter_by(id = user).first()
		for newfave in range(0, random.randrange(30)):
			s = dbsession.query(Story).filter_by(id=random.randrange(20000)).first()
			u.faves.append(s)
			
		dbsession.commit()	
		if user % 100 == 0:
			print "User " + str(user) + " faves set."

	
	print "Adding between zero and thirty reccomendations to stories"
	for stories in range(1,20000):
		story = dbsession.query(Story).filter_by(id=stories).first()
		for newrec in range(0, random.randrange(30)):
			rec = Reccomendation("this is a good story")
			rec.uid = random.randrange(99)+1 
			u = dbsession.query(User).filter_by(id = rec.uid).first()
			rec.uname = u.name
			rec.sid = story.id
			rec.date = datetime.now()
			story.recs.append(rec)
		dbsession.commit()

	



