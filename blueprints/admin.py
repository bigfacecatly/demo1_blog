

from flask import Blueprint


from bluelog.forms import PostForm
from bluelog.models import Post,Category
from bluelog.utils import redirect_back


admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
	page = request.args.get('page',1,type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).pagination(page,per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
	posts = pagination.items
	return render_template('admin/manage_post.html',pagination=pagination,posts=posts)




@admin_bp.route('/post/new',methods=['GET','PO]S'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		body = form.body.data
		category = Category.query.get(form.category.data)
		post = Post(title=title,body=body,category=category)
		db.session.commit()
		flash('Post created.','success')
		return redirect(url_for('.show_post',post_id=post.id))
	return render_template('admin/new_post.html',form=form)




#编写新建文章
@admin_bp.route('/post/<int:post_id>/edit',methods=['GET','POST'])
@login_required
def edit_post(post_id):
	form = PostForm()
	post = Post.query.get_or_404(post_id)
	if form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		post.category = Category.query.get(form.category.data)
		db.session.commit()
		flash('Post updated.','success')
		return redirect(url_for('.show_post',post_id=post.id))
	form.title.data = post.title
	form.body.data = post.body
	form.category.data = post.category_id
	return render_template('admin/edit_post.html',form=form)


#删除文章
@admin_bp.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	flash('Post deleted.','success')
	return redirect_back()

#评论开启或关闭
@admin_bp.route('/set-comment/<int:post_id>')
@login_required
def set_comment(post_id):
	post = Post.query.get_or_404(post_id)
	if post.can_comment:
		post.can_comment = False
		flash('Comment disabled.','info')
	else:
		post.can_comment = True
		flash('Comment enabled.','info')
	db.session.commit()
	return redirect(url_for('.show_post',post_id=post_id))


#批准评论
@admin_bp.route('/comment/<int:commit_id>/approve')
@login_required
def approve_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	comment.reviewed = True
	db.session.commit()
	flash('Comment published.','success')
	return redirect_back()


#评论管理
@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
	filter_rule = request.args.get('filter','all')
	page = request.args.get('page',1,type=int)
	per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
	if filter_rule == 'unread':
		filtered_comments = Comment.query.filter_by(reviewed=False)
	elif filter_rule =='admin':
		filtered_comments = Comment.query.filter_by(from_admin=True)
	else:
		filtered_comments = Comment.query

	pagination = filtered_comments.order_by(Comment.timestamp.desc()).pagination(page,per_page=per_page)
	comments = pagination.items
	return render_template('admin/manage_comment.html',comments=comments,pagination=pagination)


















