import json
from datetime import datetime, timedelta
from functools import wraps

from flask import request, jsonify, Response
from flask_jwt_extended import verify_jwt_in_request
from voluptuous import Invalid, Schema
from werkzeug.exceptions import HTTPException

from project.exceptions import ValidationError
from project.helper import load_json


def data_schema(schema: Schema, is_replace=False):
    """request json schema"""

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                json_data = schema(load_json(request.json))
                if is_replace:
                    request.json_data = json_data
            except Invalid as e:
                raise ValidationError(f'輸入參數錯誤: {e}')
            except Exception:
                raise ValidationError('請輸入正確參數')

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def args_schema(schema: Schema, is_replace=False):
    """request args schema"""

    def decorator(f):

        @wraps(f)
        def new_func(*args, **kwargs):
            try:
                json_args = schema(request.args.to_dict())
                if is_replace:
                    request.json_args = json_args
            except Invalid as e:
                raise ValidationError(f'輸入參數錯誤: {e}')
            except Exception:
                raise ValidationError('請輸入正確參數')

            return f(*args, **kwargs)

        return new_func

    return decorator


def paginate(default_per_page=10, max_per_page=50, hidden=None, hidden_info=None, public=None, extra=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            page = request.args.get('page', 1, type=int)
            per_page = default_per_page
            default_max_per_page = 100  # TODO 若要統一每頁最大筆數，搬去constant.py中

            if request.args.get('per_page'):
                per_page = min(request.args.get('per_page', max_per_page, type=int), default_max_per_page)

            query = f(*args, **kwargs)

            empty_result = {
                'data': [],
                'meta': {
                    'page': 1,
                    'per_page': per_page,
                    'total': 0,
                    'pages': 1,
                },
                'code': 200
            }

            if query is None:
                return jsonify(empty_result)

            p = query.paginate(page=page, per_page=per_page)
            pages = {
                'page': page,  # 當前頁
                'per_page': per_page,  # 每頁筆數
                'total': p.total,  # 總筆數
                'pages': p.pages,  # 共幾頁
            }
            data = []
            if hidden_info:
                for r, v in p.items:
                    tmp = {}
                    for obj in r:
                        tmp.update(obj.to_json(hidden=hidden_info.get(obj.__tablename__, None), public=public))
                    data.append(tmp)
            else:
                data = [r.to_json(hidden=hidden, public=public, extra=extra) for r in p.items]

            from flask import current_app
            print('.................', current_app.json, flush=True)

            return jsonify({
                'data': data,
                'meta': pages,
                'code': 200,
            })

        return wrapped

    return decorator


def auth_route(bp, *args, **kwargs):
    """
    被裝飾的function，需要登入才能使用
    """

    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            status = 200
            headers = {}
            verify_jwt_in_request()  # make sure login token
            rv = f(*args, **kwargs)
            rv = rv if rv else {}

            if isinstance(rv, Response):
                return rv

            # generic object (dict, model), status
            if isinstance(rv, tuple):
                if len(rv) >= 3:
                    headers = rv[2]
                status = rv[1]
                rv = rv[0] if rv[0] else {}

            return jsonify(dict(code=status, data=rv)), status, headers

        return wrapper

    return decorator


def route(bp, *args, **kwargs):
    """
    被裝飾的function，無須登入
    """
    kwargs.setdefault('strict_slashes', False)

    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            status = 200
            rv = f(*args, **kwargs)

            rv = rv if rv else {}

            if isinstance(rv, Response):
                return rv

            # (<Response>, status)
            if isinstance(rv, tuple):
                status = rv[1]
                rv = rv[0] if rv[0] else {}
                if isinstance(rv, Response):
                    return rv, status

            return jsonify(dict(code=status, data=rv)), status

        return wrapper

    return decorator


def customized_query_filter(days=7, fields='created', default_time_interval=False):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                _filters = json.loads(request.args.get('filters', '{}'))
                if not isinstance(_filters, dict):
                    raise ValidationError(f'{_filters} 格式不正确')
            except ValueError:
                _filters = {}

            if not _filters and default_time_interval is True:
                _filters[f'{fields}_ge'] = datetime.utcnow() - timedelta(days=days)

            kwargs['filters'] = _filters
            return f(*args, **kwargs)
            # try:
            #     return f(*args, **kwargs)
            # except Exception as e:
            #     raise ValidationError(f'輸入查詢參數有錯誤 {_filters}, {e=}')

        return wrapper

    return decorator


def customized_query_fields():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                _fields = request.args.get('fields', '')
                _fields = _fields.split(",")
            except ValueError:
                _fields = []

            kwargs['fields'] = _fields
            try:
                return f(*args, **kwargs)
            except Exception as e:
                raise ValidationError(f'輸入查詢參數有錯誤 {_fields}, {e=}')

        return wrapper

    return decorator


def customized_output_fields(public=None, hidden=None, extra=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            obj = f(*args, **kwargs)
            data = obj.to_json(public=public, hidden=hidden, extra=extra)
            return jsonify({
                'data': data,
                'code': 200,
            })

        return wrapper

    return decorator
