from fastapi.responses import RedirectResponse
import requests
import base64
import os

from fastapi import HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from jose import jwt, JWTError
from functools import wraps

from api import app, sso

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=os.getenv('KEYCLOAK_TOKEN_URL'), auto_error=False)

def get_rsa_public_key(jwk):
    e = int.from_bytes(base64.urlsafe_b64decode(jwk["e"] + "=="), "big")
    n = int.from_bytes(base64.urlsafe_b64decode(jwk["n"] + "=="), "big")
    public_numbers = rsa.RSAPublicNumbers(e, n)
    public_key = public_numbers.public_key(default_backend())
    return public_key

def get_public_key(token: str):
    jwks = requests.get(os.getenv('KEYCLOAK_CERTS_URL')).json()
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return get_rsa_public_key(key)
    raise HTTPException(status_code=401, detail="Public key not found")

# Token validation
def verify_auth():
    try:
        token = sso.access_token

        if not token:
            raise PermissionError()

        public_key = get_public_key(token)
        
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience='account',
            issuer=os.getenv('KEYCLOAK_URL'),
        )
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")
    
@app.get("/")
async def sso_login(request: Request):
    async with sso:
        return await sso.get_login_redirect(state=request.query_params.get('state'))

@app.get("/callback")
async def sso_callback(request: Request):
    async with sso:
        user = await sso.verify_and_process(request)

    if user is None:
        raise HTTPException(401, "Failed to fetch user information")
    
    if request.query_params.get('state'):
        return RedirectResponse(request.query_params.get('state'))
    else:
        return user.model_dump()

def authentication(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        request: Request = kwargs['request']

        try :
            payload = verify_auth()
            kwargs['request'].state.auth = payload

            return await func(*args, **kwargs)
        except PermissionError:
            return RedirectResponse(f'{request.url_for('sso_login')}?state={request.url}')
        except KeyError:
            raise HTTPException(500, "Failed to get request")

    return wrapped