class JoinvestError(Exception):
    """
    Base error
    """
    def __init__(self, message='JoinvestError'):
        super().__init__(message)


class BaseError(Exception):
    def __init__(self, msg=None, error_code=50000):
        Exception.__init__(self)
        self.code = 500  # http status code
        self.error_code = error_code  # customize code
        self.error_msg = msg

    def to_dict(self):
        return {'code': self.error_code, 'message': self.error_msg}


class ValidationError(BaseError):
    """
    客戶端錯誤
    error_code = 40001
    msg = '參數錯誤'
    type = 'invalid_request'
    """
    def __init__(self, msg=None, error_code=4001):
        BaseError.__init__(self)
        self.code = 400  # http status code
        self.error_code = error_code  # customize code
        self.error_msg = msg or '請求失敗'


class InternalError(BaseError):
    """
    基本系統錯誤
    """

    def __init__(self, msg=None, error_code=5000):
        BaseError.__init__(self)
        self.code = 500  # http status code
        self.error_code = error_code  # customize code
        self.error_msg = msg or '基本系統錯誤'
