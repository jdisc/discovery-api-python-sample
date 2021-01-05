# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from cyclonedx import models


def connect(url, accessToken, refreshToken):
    transport = RequestsHTTPTransport(url=url, verify=False, retries=3, headers={'Authorization': f'Bearer {accessToken}'})
    return Client(transport=transport, fetch_schema_from_transport=True), accessToken, refreshToken

def login(url, user, password):
    transport = RequestsHTTPTransport(url=url, verify=False, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
        """
        mutation($user: String, $password: String) {
          authentication {
            login(login: $user, password: $password) {
              status
              accessToken
              refreshToken
            }
          }
        }
        """
    )
    result = client.execute(query, variable_values={'user': user, 'password': password})
    print(result)
    return connect(url, result.get('authentication').get('login').get('accessToken'),
                   result.get('authentication').get('login').get('refreshToken'))

# return id of network
def getNetworkByIPAddress(ipaddr):
    query = gql(
        """
        query getNetworksByIPAddress($ipaddr: String) {
          networking {
            ip4Networks {
              findIP4NetworksByBaseAddress(networkBaseAddress: $ipaddr){
                id
                name
                networkBaseAddress
              }
            }
          }
        }
        """)
    result = client.execute(query, variable_values={'ipaddr': ipaddr})
    return result.get('data').get('networking').get('ip4Networks').get('findIP4NetworksByBaseAddress')[0].get('id')


def getAllSoftwareInstances(client):
    query = gql(
        """
        query getSoftwareWithInstances {
          software {
            applications {
              findAll {
                name
                version
                manufacturer
                installations {
                  installationPath
                  installationDate
                  source
                  license {
                    type
                    productId
                    productKey
                    expirationDate
                  }
                }
              }
            }
          }
        }
    """
    )
    return client.execute(query)

def buildComponents(results):
    components = []
    print(result)

    return components

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client, accessToken, refreshToken = login("https://localhost/graphql", 'Peter Klotz', 'pk')
    #with open('disocvery-api.gql') as f: schema_str = f.read()
    #client = Client(schema=schema_str)
    result = getAllSoftwareInstances(client)
    components = buildComponents(result)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
