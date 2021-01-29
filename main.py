# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import cyclonedx
from cyclonedx.models import Component
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import argparse

from packageurl import PackageURL
from cyclonedx.bom import generator


def connect(url, accessToken, refreshToken):
    transport = RequestsHTTPTransport(url=url, verify=False, retries=3, headers={'Authorization': f'Bearer {accessToken}'})
    return Client(transport=transport, fetch_schema_from_transport=True), accessToken, refreshToken

#
# authenticate with JDisc server using a mutation
#
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
    return connect(url, result.get('authentication').get('login').get('accessToken'),
                   result.get('authentication').get('login').get('refreshToken'))

# return id of network
def get_networks_by_ipaddress(ipaddr):
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

# resolve devices for network
def get_devices_for_networkdevices(networkID):
    query = gql(
        """
        query getDevicesForNetowork($network: String) {
          
        }
        """)
    result = client.execute(query, variable_values={'network': networkID})


def get_applications_for_device(deviceId):
    query = gql(
        """
        query getApplicationsForDevice($device: String) {

        }
        """)
    result = client.execute(query, variable_values={'device': deviceId})


def get_all_software_instances(client):
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

# build BOM components from applications
def build_components(results):
    components = []
    for app in results.get('software').get('applications').get('findAll'):
        comp = Component(
            name=app.get('name'),
            version=app.get('version'),
            purl=generate_purl(app.get('source'), app.get('name'), app.get('version')),
            component_type='library'
        )
        components.append(comp)

    return components

# create a PURL with reasonable defaults
def generate_purl(app_source, app_name, app_version):
    if not app_source:
        source = 'generic'
    else:
        source = app_source
    return PackageURL(source, '', app_name, app_version, '', '').to_string()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # using argparse see https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("network", nargs="+")
    parser.add_argument("-s", "--server", default="https://localhost/graphql")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--password")
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    print(f"Generate SBOM for networks {args.network}")

    # connect to server
    client, accessToken, refreshToken = login(args.server, args.user, args.password)

    # get software instances from server
    result = get_all_software_instances(client)
    if result:
        # build components of SBOM
        components = build_components(result)
        if components:
            # serialize SBOM as CycloneDX JSON
            bom = generator.build_json_bom(components)
            if args.output_file:
                out = open(args.output_file, "w", encoding="utf-8")
            else:
                out = sys.stdout
            with out:
                # output to file or stdout
                out.write(bom)
        else:
            print("failed to generate SBOM")
    else:
        print("failed to get software instances from JDisc servr")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
