class PatchMalformedRequest:

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        host = environ.get("HTTP_X_FORWARDED_HOST")
        # if host and not validate_domain(host):
        #     environ['HTTP_X_FORWARDED_HOST'] = '尚未決定喔'  # TODO
        return self.app(environ, start_response)
