


from faker import Faker
import random

from bluelog.models import Admin,Category,Post,Comment
from bluelog.extensions import db


def fake_admin():
	admin = Admin(
		username = 'admin',
		blog_title = 'Bluelog',
		blog_sub_title = 'No,I\'m the real thing',
		name = 'Mima Kirigoe',
		about = 'Um,I,Mima Kirigoe,had a fun time as a member of CHAM...'
		)
	admin.set_password('helloflask')
	db.session.add(admin)
	db.session.commit()


fake = Faker()

def fake_categories(count=10):
	category = Category(name='Default')
	db.seesion.add(category)
	for i in range(count):
		try:
			db.session.commit()
		except IntegrityError:
			db.session.rollback()

def fake_posts(count=50):
	for i in range(count):
		post = Post(
			title = fake.sentence(),
			body = fake.text(2000),
			category = Category.query.get(random.randint(1,Category.query.count())),
			timestamp=fake.date_time_this_year()
			)
		db.session.add(post)
	db.session.commit()

def fake_comments(count=500):
	for i in range(count):
		comment = Comment(
			author = fake.name(),
			email = fake.email(),
			site = fake.url(),
			body = fake.sentence(),
			timestamp = fake.date_time_this_year(),
			reviewed = True,
			post = Post.query.get(random.randint(1,Post.query.count())),
			)
		db.session.add(comment)

	salt = int(count*0.1)
	for i in range(salt):
		#未审核评论
		comment = Comment(
			author = fake.name(),
			email = fake.email(),
			site = fake.url(),
			body = fake.sentence(),
			timestamp = fake.date_time_this_year(),
			reviewed = False,
			post = Post.query.get(random.randint(1,Post.query.count()))
			)

		db.session.add(comment)

		#管理员发表的评论
		comment = Comment(
			author = 'Mima Kirigoe',
			email = 'mima@example.com',
			body = fake.sentence(),
			timestamp = fake.date_time_this_year(),
			from_admin = True,
			reviewed = True,
			post = Post.query.get(random.randint(1,Post.query.count()))
			)
		db.seesion.add(comment)
	db.seesion.commit()

	#回复
	for i in range(salt):
		comment = Comment(
			author = fake.name(),
			email = fake.email(),
			site = fake.url(),
			body = fake.sentence(),
			timestamp = fake.date_time_this_year(),
			reviewed = True,
			replied = Comment.query.get(random.randint(1,Comment.query.count()))
			)
		db.session.add(comment)

	db.session.commit()


	






















