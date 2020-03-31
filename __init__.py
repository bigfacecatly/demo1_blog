
from flask import Flask
from flask_wtf.csrf import CSRFError

from bluelog.settings import config
from bluelog.extensions import bootstrap,db,moment,cheditor,mail
from bluelog.models import Admin,Category


def create_app(config_name=None):
	if config_name  is None:
		config_name = os.getenv('FLASK_CONFIG','development')

	app = Flask('bluelog')
	app.config.from_object(config[config_name])

	register_logging(app)
	register_extensions(app)
	register_blueprints(app)
	register_commands(app)
	register_errors(app)
	register_shell_context(app)
	register_template_context(app)
	return app

def register_logging(app):
	pass

def register_extensions(app):
	bootstrap.init_app(app)
	db.init_app(app)
	cheditor.init_app(app)
	mail.init_app(app)
	moment.init_app(app)

def register_blueprints(app):
	app.register_blueprint(blog_bp)
	app.register_blueprint(admin_bp,url_prefix='/admin')
	app.register_blueprint(auth_bp,url_prefix='/auth')

def register_shell_context(app):
	@app.shell_context_processor
	def make_shell_context():
		return dict(db=db)

def register_errors(app):
	@app.errorhandler(400)
	def bad_request(e):
		return render_template("errors/400.html"),400


def reigster_commands(app):
	

	@app.cli.command()
	@click.option('--username',prompt=True,help='The username used to login.')
	@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login.')
	def init(username,password):
		""" Building Bluelog,just for you """
		click.echo('Initializing the database')
		db.create_all()

		admin = Admin.query.first()
		if admin:
			click.echo('The administrator aleady exists,updating...')
			admin.username = username
			admin.set_password(password)
		else:
			click.echo('Creating the temporary administrator accunt...')
			admin = Admin(
				username = username,
				blog_title = 'Bluelog',
				blog_sub_title = "No,I'm the real thing.",
				name = 'Admin',
				about = 'Anything about you.'
				)
			admin.set_password(password)
			db.session.add(admin)

		category = Category.query.first()
		if category is None:
			click.echo('Creating the default category...')
			category = Category(name='Default')
			db.session.add(category)
		db.session.commit()
		click.echo('Done.')



def register_template_context(app):
	@app.content_processor
	def make_template_context():
		admin = Admin.query.first()
		categories = Category.query.order_by(Category.name).all()
		return dict(admin=admin,categories=categories)
	


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
	return render_template('errors/400.html',description=e.description),400


























