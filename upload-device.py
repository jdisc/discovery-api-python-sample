# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import jdisc

from gql import Client, gql
import argparse


# upload a device
def upload_device(client, device):
    query = gql(
        """
        mutation {
          importManager {
            importDevice(device: { 

              }
            }
          }
        }
        """)
    result = client.execute(query, variable_values={'device': device})
    return result.get('data').get('errors')


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
    client, accessToken, refreshToken = jdisc.login(args.server, args.user, args.password)

    # read content from file
    upload_device(client, device)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
