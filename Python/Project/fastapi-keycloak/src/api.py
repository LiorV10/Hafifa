import os
from typing import Any, Union
from fastapi import FastAPI, HTTPException
from fastapi_sso.sso.generic import create_provider
from fastapi_sso.sso.base import DiscoveryDocument, OpenID
from httpx import AsyncClient

def convert_openid(response: dict[str, Any], _client: Union[AsyncClient, None]) -> OpenID:
    """Convert user information returned by OIDC"""
    return OpenID(id=response['sub'], display_name=response['name'], **response)


discovery_document: DiscoveryDocument = {
    "authorization_endpoint": os.getenv('KEYCLOAK_AUTHORIZATION_URL'),
    "token_endpoint": os.getenv('KEYCLOAK_TOKEN_URL'),
    "userinfo_endpoint": os.getenv('KEYCLOAK_USERINFO_URL'),
}

GenericSSO = create_provider(name="oidc", discovery_document=discovery_document, response_convertor=convert_openid)

sso = GenericSSO(
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    redirect_uri="http://localhost:8000/callback",
    scope="openid email profile",
    allow_insecure_http=True
)

app = FastAPI()