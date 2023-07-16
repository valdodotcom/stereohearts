from rest_framework.authtoken.models import Token

def get_session_key(request):
    authorization_header = request.headers.get('Authorization', '')
    session_key = None

    if request.user.is_authenticated:
        try:
            session_key = request.user.auth_token.key
        except AttributeError:
            pass

    if session_key is None:
        try:
            token = authorization_header.split(' ')[1]
            if Token.objects.filter(key=token).exists():
                session_key = token
        except IndexError:
            pass
    # print(session_key)
    # print(authorization_header)
    return session_key