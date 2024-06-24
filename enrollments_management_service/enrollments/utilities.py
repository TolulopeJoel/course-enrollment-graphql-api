import requests
# from django.http.

API_GATEWAY_URL = "http://gateway:4001/graphql"


def verify_token(token):
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
    if errors := response.json().get('errors'):
        raise Exception("Signature has expired")
    return 'payload' in response.json().get('data', {}).get('verifyToken')


def get_user_from_token(token):
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

    print(response.json(), 22)

    if response.status_code == 200:
        return response.json().get('data', {}).get('whoami')
