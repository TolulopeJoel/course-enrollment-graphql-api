import requests

API_GATEWAY_URL = "http://gateway:4001/graphql"

def check_user_exists(token):
    query = """
    query {
        whoami {
            id
            email
        }
    }
    """
    response = requests.post(
        API_GATEWAY_URL,
        json={'query': query},
        headers={'Authorization': token}
    )

    if response.status_code == 200:
        return response.json().get('data', {}).get('whoami')


def validate_token(token):
    # Remove 'Bearer ' prefix if present
    if token.startswith('Bearer '):
        token = token[7:]

    query = """
    mutation($token: String!) {
        verifyToken(token: $token)
    }
    """
    variables = {'token': token}
    response = requests.post(
        API_GATEWAY_URL,
        json={'query': query, 'variables': variables}
    )
    return 'payload' in response.json().get('data', {}).get('verifyToken')
