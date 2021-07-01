"""
Consumer example app
"""
import ast
import json
import time

from arrowhead_client.client.implementations import SyncClient
import urllib3

import settings_client
from mariadb_operations import insert_mariadb_arrowhead
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

consumer = SyncClient.create(
    system_name=settings_client.consumer2_systemname,
    address=settings_client.consumer2_address,
    port=settings_client.consumer2_port,
    keyfile=settings_client.consumer2_keyfile,
    certfile=settings_client.consumer2_certfile,
    cafile=settings_client.consumer2_cafile,
)

if __name__ == '__main__':
    conn = None
    consumer.setup()

    consumer.add_orchestration_rule(settings_client.consumer2_consumer_service_name, 'GET')
    # response = consumer.consume_service('tribune1',verify='C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/provider1.ca')

    response = consumer.consume_service(settings_client.consumer2_consumer_service_name,
                                        verify=False)
    while True:
        time.sleep(5)
        response = consumer.consume_service(settings_client.consumer2_consumer_service_name,
                                            verify=False)
        print(response.payload.decode('utf8'))
        json_data = json.dumps(ast.literal_eval(response.payload.decode('utf8')))
        json_final_as_dict = json.loads(json_data)
        if response is not None:
            insert_mariadb_arrowhead(conn, settings_client.consumer2_database_tablename, json_final_as_dict)
