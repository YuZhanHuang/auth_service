import os

from werkzeug import run_simple

from project import create_app

app = create_app()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH')
    response.headers.add('Access-Control-Max-Age', '3600')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.cache_control.max_age = 1
    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    run_simple(
        '0.0.0.0',
        port,
        app,
        threaded=True,
        use_reloader=True,
        use_debugger=True)
