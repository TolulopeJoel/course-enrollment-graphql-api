import requests


API_GATEWAY_URL = "http://gateway:4001/graphql"


def verify_token(token):
    response = requests.post(
        API_GATEWAY_URL,
        json={
            'query': '''
            mutation($token: String!) {
                verifyToken(token: $token)
            ''',
            'variables': {'token': token}
        },
        headers={'Content-Type': 'application/json'}
    )
    result = response.json()
    return 'errors' not in result
