"""
Provider example app
"""
import csv
import time
import sys
sys.path.append('/root/client-program/client-library-python/examples/quickstart/clients')
sys.path.append('/root/client-program/client-library-python/examples/quickstart')
sys.path.append('/root/client-program/client-library-python')
from arrowhead_client.client.implementations import SyncClient
import settings_client
import ssl
ssl.match_hostname = lambda cert, hostname: True

provider = SyncClient.create(
    system_name=settings_client.provider5_system_name,
    address=settings_client.provider5_address,
    port=settings_client.provider5_port,
    keyfile=settings_client.provider5_keyfile,
    certfile=settings_client.provider5_certfile,
    cafile=settings_client.provider5_cafile,
)

i = 0
start = time.perf_counter()


def csv_to_json(csvFilePath):
    jsonArray = []

    # read csv file
    with open(csvFilePath, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvReader:
            # add this python dict to json array
            jsonArray.append(row)

        # jsonString = json.dumps(jsonArray, indent=4)
        return jsonArray


data_set_json = csv_to_json(settings_client.provider5_csv_excel_file)
finish = time.perf_counter()
print(f"Conversion 52.706 rows completed successfully in {finish - start:0.4f} seconds")


@provider.provided_service(
    service_definition=settings_client.provider5_service_definition,
    service_uri=settings_client.provider5_service_uri,
    protocol=settings_client.provider5_service_protocol,
    method=settings_client.provider5_service_method,
    payload_format=settings_client.provider5_payload_format,
    access_policy=settings_client.provider5_access_policy, )
def hello_arrowhead(request):
    global i
    i = i + 1
    if i < len(data_set_json):
        return str(data_set_json[i])
    else:
        return None


if __name__ == '__main__':
    provider.run_forever()
