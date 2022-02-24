import json
from flask import Flask, request, _request_ctx_stack,abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

app = Flask(__name__)

AUTH0_DOMAIN = 'dev-f81imyrd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Capstone'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
   auth = request.headers.get("Authorization",None)
   if not auth:
        abort(401)
   
   method = auth.split()
   
   if method[0].lower() != 'bearer':
       raise Exception('authorization header must start with bearer') 
   
   if len(method)!=2:
       raise Exception('token not found or authorization header invalid')
   
   token = method[1]
   return token         

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        abort(403)    
    
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(token,rsa_key,
            algorithms=ALGORITHMS,audience=API_AUDIENCE,
            issuer='https://'+ AUTH0_DOMAIN + '/') 

            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)         
 
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
        
            try:
                payload = verify_decode_jwt(token)

            except:
                abort(401)
            
            check_permissions(permission, payload)
            
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
