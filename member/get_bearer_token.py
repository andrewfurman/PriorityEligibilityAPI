# get_bearer_token.py

# the get bearer token function Will get a valid bar token from the AWS Cognito service using the environment variables for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, COGNITO_USER_POOL_ID, COGNITO_APP_CLIENT_ID and then return the bearer token as a string.

import os
import boto3
from botocore.exceptions import ClientError

def get_bearer_token() -> str:
    """
    Gets a bearer token from AWS Cognito using environment variables.
    Returns:
        str: Bearer token (AccessToken) from Cognito
    Raises:
        Exception: If authentication fails or environment variables are missing
    """
    try:
        # Get required environment variables
        user_pool_id = os.environ['COGNITO_USER_POOL_ID']
        client_id = os.environ['COGNITO_APP_CLIENT_ID']
        region = os.environ['AWS_DEFAULT_REGION']
        username = os.environ.get('COGNITO_USERNAME')
        password = os.environ.get('COGNITO_PASSWORD')

        if not username or not password:
            raise Exception("COGNITO_USERNAME and COGNITO_PASSWORD environment variables are required")

        # Initialize Cognito Identity Provider Client
        cognito_client = boto3.client('cognito-idp',
            region_name=region,
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )

        # Authenticate with Cognito
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId=client_id
        )

        # Return only the AccessToken
        return response['AuthenticationResult']['AccessToken']
    except Exception as e:
        raise Exception(f"Failed to get bearer token: {str(e)}")

if __name__ == "__main__":
    try:
        token = get_bearer_token()
        print(token)
    except Exception as e:
        print(f"Error: {str(e)}")