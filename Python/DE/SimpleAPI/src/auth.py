from dotenv import load_dotenv

load_dotenv(override=True)

from fastapi_keycloak_middleware import KeycloakConfiguration

import os

keycloak_config = KeycloakConfiguration(
    url=os.getenv('KEYCLOAK_HOST'),
    realm=os.getenv('KEYCLOAK_REALM'),
    client_id=os.getenv('KEYCLOAK_CLIENT_ID'),
    client_secret=os.getenv('KEYCLOAK_CLIENT_SECRET')
)