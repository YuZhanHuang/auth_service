

def get_ip(request):
    req_env = request.environ
    return req_env.get('HTTP_X_REAL_IP',
                       req_env.get("X_FORWARDED_FOR", request.remote_addr))