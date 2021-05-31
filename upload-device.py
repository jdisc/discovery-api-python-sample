# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import jdisc
import json
from gql import Client, gql
import argparse


# upload a device
def upload_device(client, device):
    query = gql(
        """
        mutation($device: DeviceInput) {
          importManager {
            importDevice(device: $device) {
              warnings
              errors
            }
          }
        }
        """)
    result = client.execute(query, variable_values={'device': device})
    return result.get('importManager').get('importDevice').get('errors')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # using argparse see https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", default="https://localhost/graphql")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--password")
    parser.add_argument("-f", "--file", required=True)
    args = parser.parse_args()
    print(f"Upload device from $file")

    # connect to server
    client, accessToken, refreshToken = jdisc.login(args.server, args.user, args.password)

    # read content from file
    with open(args.file, 'r') as file:
        device = json.loads(file.read())
    errors = upload_device(client, device)
    if errors != []:
        print("ERROR: ", errors)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
