from project.constants import DEFAULT_PASSWORD
from project.core import Service, bcrypt
from project.users.model import User


class UserService(Service):
    __model__ = User

    @staticmethod
    def _preprocess_params(kwargs):
        """preprocess params before create/update an orm object"""
        kwargs.pop('csrf_token', None)
        default_password = bcrypt.generate_password_hash(DEFAULT_PASSWORD).decode('utf-8')
        if kwargs.get('password'):
            kwargs['password'] = bcrypt.generate_password_hash(kwargs['password']).decode('utf-8')
        else:
            kwargs['password'] = default_password

        return kwargs
