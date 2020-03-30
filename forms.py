

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,Booleanield,SelectField,ValidationError,TextAreaField,HiddenField
from wtforms.validators import DataRequired,Length,Email,URL,Optional
from flask_ckeditor import CKEditorField


from bluelog.models import Category




class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(1,20)])
	password = PasswordField('Password',validators=[DataRequired(),Length(1,20)])
	remember = Booleanield('Remember me')
	submit = SubmitField('Log in')


class PostForm(FlaskForm):
	title = StringField('Title',validators=[DataRequired(),Length(1,60)])
	category = SelectField('Category',coerce=int,default=1)
	body = CKEditorField('Body',validators=[DataRequired()])
	submit = SubmitField()

	def __init__(self,*args,**kwargs):
		super(PostForm,self).__init__(*args,**kwargs)
		self.category.choices = [(category.id,category.name) for category in Category.query.order_by(Category.name).all()]

class CategoryForm(FlaskForm):
	name = StringField('Name',validators=[DataRequired(),Length(1,30)])
	submit = SubmitField()

	def validate_name(self,field):
		if Category.query.filter_by(name=field.data).first():
			raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
	author = StringField('Name',validators=[DataRequired(),Length(1,30)])
	email = StringField('Email',validators=[DataRequired(),Email(),Length(1,254)])
	body = TextAreaField('Comment',validators=[DataRequired()])
	submit = SubmitField()


class AdminCommentForm(CommentForm):
	author = HiddenField()
	email = HiddenField()
	site = HiddenField()








	





