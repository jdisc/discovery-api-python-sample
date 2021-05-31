# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import jdisc

import cyclonedx
from cyclonedx.models import Component
from gql import Client, gql
import argparse
import csv

from packageurl import PackageURL
from cyclonedx.bom import generator



#
# authenticate with JDisc server using a mutation
#

# return id of network
def get_rmon_log(client, device):
    query = gql(
        """
            query getRMONLogs($device: String) {
              devices {
                findByName(name: $device) {
                  id
                  model
                  type
                  arrayAttributes {
                    lastUpdate
                    customAttribute{
                      name
                      description
                      attributeType
                    }
                    array{
                      columnHeaders
                      rows{
                        values
                      }
                    }
                  }
                }
              }
            }
        """)
    result = client.execute(query, variable_values={'device': device})
    return result.get('devices').get('findByName')[0]

def output_as_csv(result, output_file):
    with open('eggs.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(output_file, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(",".join(result.get('arrayAttributes')[0].get('array').get('columnHeaders')))
        for row in result.get('arrayAttributes')[0].get('array').get('rows'):
            csv_writer.writerow(",".join(map(str,row.get('values'))))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # using argparse see https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument("device")
    parser.add_argument("-s", "--server", default="https://localhost/graphql")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--password")
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    print(f"Get RMON log {args.device}")

    # connect to server
    client, accessToken, refreshToken = jdisc.login(args.server, args.user, args.password)

    # get software instances from server
    result = get_rmon_log(client, args.device)
    if result:
        # output log
        output_file = args.output_file
        if not output_file:
            output_file = sys.stdout
        output_as_csv(result, output_file)
    else:
        print("failed to get logs")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
