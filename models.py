

from bluelog.extensions import db
from datetime import datetime

class Admin(db.Model):  
	#用户表--管理员
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(20))
	password_hash = db.Column(db.String(128))
	blog_title = db.Column(db.String(100))
	blog_sub_title = db.Column(db.String(100))
	name = db.Column(db.String(30))
	about = db.Column(db.Text)


class Category(db.Model):
	#分类
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(30),unique=True)
	posts = db.relationship('Post',back_populates='category')


class Post(db.Model):
	#文章
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(60))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime,default=datetime.utcnow)
	category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
	category = db.relationship('Category',back_populates='posts')
	Comment = db.relationship('Comment',backref='post',cascade='all,delete-orphan')

class Comment(db.Model):
	#评论
	id = db.Column(db.Integer,primary_key=True)
	author = db.Column(db.String(30))
	email = db.Column(db.String(254))
	site = db.Column(db.String(255))
	body = db.Column(db.Text)
	from_admin = db.Column(db.Boolean,default=False)
	reviewed = db.Column(db.Boolean,default=False)
	timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
	post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
	post = db.relationship('Post',back_populates='comments')
	#邻接关系
	replid_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
	replid = db.relationship('Comment',back_populates='replies',remote_side=[id])
	replies = db.relationship('Comment',back_populates='replied',cascade='all')
















