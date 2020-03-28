
from flask import Flask
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
	pass


def register_template_context(app):
	@app.content_processor
	def make_template_context():
		admin = Admin.query.first()
		categories = Category.query.order_by(Category.name).all()
		return dict(admin=admin,categories=categories)
	




























