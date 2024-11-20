# auth/token_verification.py
import os, json
import requests
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.algorithms import RSAAlgorithm

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        app_client_id = os.environ.get('COGNITO_APP_CLIENT_ID')

        region = user_pool_id.split('_')[0]
        keys_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'

        response = requests.get(keys_url)
        keys = response.json()['keys']
        headers = jwt.get_unverified_header(token)

        key_index = next((index for (index, k) in enumerate(keys) if k["kid"] == headers["kid"]), None)
        if key_index is None:
            raise Exception('Public key not found in jwks.json')

        public_key = keys[key_index]
        public_key_pem = RSAAlgorithm.from_jwk(json.dumps(public_key))

        decoded = jwt.decode(
            token,
            key=public_key_pem,
            algorithms=['RS256'],
            options={
                'verify_aud': False,
                'verify_exp': True,
                'verify_iss': True
            }
        )

        if decoded.get('client_id') != app_client_id:
            raise Exception('Token was not issued for this client_id')

        return decoded

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials: {str(e)}"
        )