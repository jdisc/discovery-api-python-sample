#
# reusable library of functions for JDisc API
#
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport


def connect(url, accessToken, refreshToken):
    transport = RequestsHTTPTransport(url=url, verify=False, retries=1, headers={'Authorization': f'Bearer {accessToken}'})
    return Client(transport=transport, fetch_schema_from_transport=True), accessToken, refreshToken


def login(url, user, password):
    transport = RequestsHTTPTransport(url=url, verify=False, retries=1)
    client = Client(transport=transport, fetch_schema_from_transport=False)
    query = gql(
        """
        mutation($user: String, $password: String) {
          authentication {
            login(login: $user, password: $password) {
              status
              accessToken
              refreshToken
              rights
            }
          }
        }
        """
    )
    result = client.execute(query, variable_values={'user': user, 'password': password})
    return connect(url, result.get('authentication').get('login').get('accessToken'),
                   result.get('authentication').get('login').get('refreshToken'))

def logout(client, accessToken):
    query = gql(
        """
        mutation($token: String) {
          authentication {
            logout(accessToken: $token) 
          }
        }
        """
    )
    return client.execute(query, variable_values={'token': accessToken})
# eof
