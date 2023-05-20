from flask import Blueprint

from project.decorators import route, customized_query_filter, paginate
from project.logger import get_logger
from project.services import users

users_bp = Blueprint('users', __name__, url_prefix='/users')
logger = get_logger(__name__)


@route(users_bp, '/', methods=["GET"])
@customized_query_filter(default_time_interval=False)
@paginate(20)
def retrieve_staffs(filters):
    return users.search(filters)
