import os
from uuid import uuid4

from flask import Flask, g, has_request_context, request

from project.config import configs
from project.helper import register_blueprints, JSONEncoder
from project.core import db, cors, jwt_manager, mail, migrate
from project.timetools import get_milliseconds
from project.utils import get_ip

root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(root_dir, 'auth_service', 'templates')


def create_app(package_name, package_path=None, settings_override=None):
    config_name = os.environ.get('FLASK_CONFIG', 'development')

    # instantiate the app
    app = Flask(package_name, template_folder=template_dir)

    # set config
    app.config.from_object(configs[config_name])
    app.json_encoder = JSONEncoder

    print('>>>>>>>>>>>>', app.json_provider_class, flush=True)
    print('iiiiiiiiiiii', app.json, dir(app.json), flush=True)

    if settings_override:
        app.config.from_object(settings_override)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    cors.init_app(app,
                  resources={r"/": {"origins": "*"}},
                  allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
                  supports_credentials=True)
    mail.init_app(app)

    # register blueprint
    if package_path:
        register_blueprints(app, package_name, package_path)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


def init_globals(app):
    g.request_id = uuid4().hex
    g.request_start_time = get_milliseconds()

    if has_request_context():
        g.client_ip = get_ip(request)
        g.user_agent = request.user_agent.string

