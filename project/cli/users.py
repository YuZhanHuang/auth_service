import click
from flask import Blueprint

from project.services import users

users_cli_bp = Blueprint('users_cli', __name__)


@users_cli_bp.cli.command('retrieve')
@click.option('--user_id', help='用戶ID')
@click.option('--username', help='用戶名字')
def retrieve_staffs(user_id=None, username=None):
    filters = {}
    if user_id:
        filters['user_id'] = int(user_id)
    if username:
        filters['username'] = str(username)
    if not filters:
        print('Please give user id or username.')
        return

    for user in users.find(**filters):
        print(f'user id {user.id} | username {user.username}')

