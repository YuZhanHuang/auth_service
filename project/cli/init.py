from flask import Blueprint

from project.core import db
from project.services import users

init_cli_bp = Blueprint('init', __name__)


@init_cli_bp.cli.command('create_all')
def db_create_all():
    """
        create all tables
    """
    print('=== create db schema and init data ===')
    db.create_all()
    init_data()
    print('=== all db schema and data finished ===')


@init_cli_bp.cli.command('create_data')
def init_only_data():
    print('=== init data ===')
    init_data()
    print('=== init data finished ===')


def init_data():
    init_staff()


def init_staff():
    print('****** init users ******')
    users_list = [
        {
            "username": "joe", "email": "joe@gamil.com",
            "password": "12345678", "email_confirm": True, "verified": True,
        },
        {
            "username": "riz", "email": "riz@gamil.com",
            "password": "12345678", "email_confirm": True, "verified": True,
        },
        {
            "username": "wayne", "email": "wayne@gamil.com",
            "password": "12345678", "email_confirm": True, "verified": True,
        },
        {
            "username": "sharon", "email": "sharon@gamil.com",
            "password": "12345678", "email_confirm": True, "verified": True,
        },
        {
            "username": "nick", "email": "nick@gamil.com",
            "password": "12345678", "email_confirm": True, "verified": True,
        },
    ]
    for user in users_list:
        users.create(**user)
        print(f"create staff - {user['username']}")
    print('****** init users finished ******')
