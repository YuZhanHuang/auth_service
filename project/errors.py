from flask import jsonify, Blueprint

from project.core import jwt_manager
from project.logger import get_logger

errors = Blueprint('errors', __name__)
logger = get_logger(__name__)


def api_on_404(e):
    """API 404 錯誤處理"""

    return jsonify(
        dict(message='not found', type="invalid_request", code=404)), 404


def api_on_429(e):
    """API 429 錯誤處理"""
    return jsonify(
        dict(message="請求過於頻繁", type="rate_limit", payload={}, code=429)), 429


def on_api_error(e):
    logger.error('on_api_error', msg=str(e), exc_info=True)
    return jsonify(e.to_dict()), e.code


@errors.app_errorhandler(Exception)
def on_base_api_error(e):
    logger.error('on_base_api_error', msg=str(e), exc_info=True)
    return jsonify({'code': 5000, 'msg': 'Internal Service Error'}), 500


@jwt_manager.expired_token_loader
def handle_expired_token_error(_jwt_header, _jwt_data):
    error_info = {'code': 4003,
                  'message': 'token已經過期'}
    return jsonify(error_info), 403


@jwt_manager.invalid_token_loader
def handle_invalid_token(e):
    error_info = {'code': 4003,
                  'message': ''}
    return jsonify(error_info), 403


@jwt_manager.unauthorized_loader
def handle_jwt_no_authorization(e):
    error_info = {'code': 4003,
                  'message': 'jwt驗證失敗'}
    return jsonify(error_info), 403


@jwt_manager.revoked_token_loader
def handle_jwt_revoked_token(e, *args):
    error_info = {'code': 4003,
                  'message': 'token已經被撤銷'}
    return jsonify(error_info), 403


@jwt_manager.token_verification_failed_loader
def handle_jwt_kick_out(*args):
    error_info = {'code': 4003,
                  'message': '帳號已在其他地方登入，系統僅允許在一個裝置登入'}
    return jsonify(error_info), 403
