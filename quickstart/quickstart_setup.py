import subprocess
import requests
import time
from typing import List

from arrowhead_client.dto import DTOMixin
from arrowhead_client.rules import OrchestrationRule
from arrowhead_client.service import ServiceInterface
from arrowhead_client.system import ArrowheadSystem
from arrowhead_client.service import Service
from arrowhead_client.client.core_system_defaults import default_config
from arrowhead_client.client.core_service_forms.client import ServiceRegistrationForm
from arrowhead_client.client.implementations import SyncClient


with requests.Session() as session:
    session.verify = 'C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/sysop.ca'
    session.cert = ('C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/sysop.crt', 'C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/sysop.key')
    is_online = [False, False, False]
    print('Waiting for core systems to get online (might take a few minutes...)')
    while True:
        try:
            if not is_online[0]:
                session.get('https://68.183.7.98:8443/serviceregistry/echo')
                is_online[0] = True
                print('Service Registry is online')
            if not is_online[1]:
                session.get('https://68.183.7.98:8441/orchestrator/echo')
                is_online[1] = True
                print('Orchestrator is online')
            if not is_online[2]:
                session.get('https://68.183.7.98:8445/authorization/echo')
                is_online[2] = True
                print('Authorization is online')
        except Exception:
            time.sleep(2)
        else:
            print('All core systems are online\n')
            break

setup_client = SyncClient.create(
        system_name='sysop',
        address='',
        port=1337,
        keyfile='C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/sysop.key',
        certfile='C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/sysop.crt',
        cafile='C:/Users/oguzhan.herkiloglu/PycharmProjects/client-library-python/examples/quickstart/certificates/crypto/sysop.ca'
)

print('Setting up local cloud')

setup_client.orchestration_rules.store(
        OrchestrationRule(
                Service(
                        'mgmt_register_service',
                        'serviceregistry/mgmt',
                        ServiceInterface.from_str('HTTP-SECURE-JSON'),
                ),
                ArrowheadSystem(
                        **default_config['service_registry']
                ),
                'POST',
        )
)

setup_client.orchestration_rules.store(
        OrchestrationRule(
                Service(
                        'mgmt_get_systems',
                        'serviceregistry/mgmt/systems',
                        ServiceInterface('HTTP', 'SECURE', 'JSON'),
                ),
                ArrowheadSystem(
                        **default_config['service_registry']
                ),
                'GET',
        )
)

setup_client.orchestration_rules.store(
        OrchestrationRule(
                Service(
                        'mgmt_register_system',
                        'serviceregistry/mgmt/systems',
                        ServiceInterface('HTTP', 'SECURE', 'JSON'),
                ),
                ArrowheadSystem(
                        **default_config['service_registry']
                ),
                'POST',
        )
)

setup_client.orchestration_rules.store(
        OrchestrationRule(
                Service(
                        'mgmt_orchestration_store',
                        'orchestrator/mgmt/store',
                        ServiceInterface('HTTP', 'SECURE', 'JSON'),
                ),
                ArrowheadSystem(
                        **default_config['orchestrator']
                ),
                'POST',
        )
)

setup_client.orchestration_rules.store(
        OrchestrationRule(
                Service(
                        'mgmt_authorization_store',
                        'authorization/mgmt/intracloud',
                        ServiceInterface('HTTP', 'SECURE', 'JSON'),
                ),
                ArrowheadSystem(
                        **default_config['authorization']
                ),
                'POST',
        )
)

setup_client.setup()

consumer_system = ArrowheadSystem(
        system_name='consumer1',
        address='',
        port=7656
)
provider_system = ArrowheadSystem(
        system_name='producer1',
        address='',
        port=7655,
        authentication_info='MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdgb87lp4H/XSJxzzpBC7nF/2GwMpXK2xd3KrcpnrF460+qwbURwjevNhlc1FOZ+tyLQy7SCcVMr+xVFubcKKj6H063ojjePBfRYNXkaN/E5xyKdTvrXNpjcwTaM7POelImPtqwiPpDb4JV/xj0Q2EYlRdxYca+sNGsVU37X3/EGMS3eZpiWRIs3fBGNyztpVGC8RiAEoqeuxFZWI0J3E9gx5hDQw2/Bx8tofESZvAQJcUCevhAhXtx5oiGpk6Fym9SgygMIQpkh4pnWAsZonZY1l1tBzQ19CLaxkc0QM1t2cBx1i8dUKvyfsfmZbgzfKRJzNDKKvT1FHtUEZmv/HFAgMBAAECggEBAIjFWxbWcoIDsEfX7+dzz3qy1V9HWC0bsu1KqkASfHgMfar2fmalDGnGWK631XmdOdGalvyl6fI5cEX/N9EhnMlyIBSXmwzUPv6r8SKAgBXgJLDp7FL4LkkRbY3JLBS8d/unhGKvFNnSKhwZADx5EyDK9fG7jdd6u0lOwe5f11I9OjaGX5dp1bP5GrYDjx2TZklCuqeo3YqYOgR1ruTa/ruw13qbq+KY4YQlVbryDaDjPaOhZg7yJRrYWR1jjRSRY23k5xzVhlrwbjITsBg7F/pq/j7ADZmtA7eFiiLf6IlGDUCnxjNS40N/rWJe9Qg2W0DuW2rSHJYGS2ZvMJbK7T0CgYEA7GS/legq3u2geXKALGwzfIg1eOOLOijq3aGDp+ohODZPQTNgr3+jnQsVfZQcXdoZprs4DlqjjQWy8Nprjmvn2WZY+MbNEyKr6EX+Q9j3EGMuFNcpJpQHhQx2G97cda3DQ/VqPkk7XjITsXWnaeG4+5RLghgBgGRL9ptWecnOlEMCgYEAqpIHF9lNXjKt6ToYkZzytRJidznLs3QpJz90wtjio0AgnCpVtQOnPMuZEbVRL53pqL3pkaBMFQOavI1pHee2EE7X0/NQfSXoYxrZWc0ykvTY8bb7OPx2DPBJ7NyHTXkPr/LkwOZaggO/N7XiHDGv7/pYZmCQkxeH4enyiMN8xVcCgYB/ArKdTJycIniyR/7t30TaiCSSy08m9I0cf4dJVNZ8aVGz6nLsWFwEKMxnKIkFNAXMO5MmwzRUtNcr6W8Ymol7mS38nHPa8CoFJnYy5gP43hEISYJmo+pWZhefaeJxp+beQKHQzXAEcEt8cYZ9sTW+ljLrtxI3dawK1/NihDdmGQKBgBmO3/k22lzvAxgbWGsZNVTkeFSdGGS/VxtGatx3Wx5TEY/U2BrTfU+iwkDhBlU4ODbMnh7wAfZ0H8948PNGMQWoirZ7kuftsjCHaWIHWTij743oeSREz/uIVctkD/IP3cXjg1tUKOOqZBCY9FR9LXur62sLtR4VPIshXvIXOK7pAoGBAKZS8kiRNu9EIRo6gj62y6SEgCk/+yqbmafU35wBGz51BbNbdsSMLEJxpSQv1KFjRlHbyzTo1OnLOeel2WsJh+b0c4+q/dPpChFqmXkucccpusEw2lDdoRz1rT+R9Q8IFcE6583DrIRAedAS4NvFbAxBg4b/kybxaA5Zv1xBNHcQ',)

consumer_data = setup_client.consume_service(
        'mgmt_register_system', json=consumer_system.dto()
).read_json()
provider_data = setup_client.consume_service(
        'mgmt_register_system', json=provider_system.dto()
).read_json()

systems = {
    'consumer1': (ArrowheadSystem.from_dto(consumer_data), consumer1_data['id']),
    'producer1': (ArrowheadSystem.from_dto(provider_data), producer1_data['id']),
}

hello_form = ServiceRegistrationForm.make(
        Service(
                'hello-arrowhead',
                'hello',
                ServiceInterface.from_str('HTTP-SECURE-JSON'),
                'CERTIFICATE',
        ),
        systems['producer1'][0],
)
echo_form = ServiceRegistrationForm.make(
        Service(
                'echo',
                'echo',
                ServiceInterface.from_str('HTTP-SECURE-JSON'),
                'CERTIFICATE',
        ),
        systems['producer1'][0],
)

hello_res = setup_client.consume_service(
        'mgmt_register_service',
        json=hello_form.dto(),
).read_json()
echo_res = setup_client.consume_service(
        'mgmt_register_service',
        json=echo_form.dto(),
).read_json()
hello_id = hello_res['serviceDefinition']['id']
echo_id = echo_res['serviceDefinition']['id']


class OrchestrationMgmtStoreForm(DTOMixin):
    service_definition_name: str
    consumer_system_id: str
    provider_system: ArrowheadSystem
    service_interface_name: str
    priority: int = 1


hello_orch_form = OrchestrationMgmtStoreForm(
        service_definition_name='hello-arrowhead',
        consumer_system_id=systems['consumer1'][1],
        provider_system=systems['producer1'][0],
        service_interface_name='HTTP-SECURE-JSON',
)
echo_orch_form = OrchestrationMgmtStoreForm(
        service_definition_name='echo',
        consumer_system_id=systems['consumer1'][1],
        provider_system=systems['producer1'][0].dto(),
        service_interface_name='HTTP-SECURE-JSON',
)

res = setup_client.consume_service(
        'mgmt_orchestration_store',
        json=[hello_orch_form.dto(), echo_orch_form.dto()]
)


class AuthorizationIntracloudForm(DTOMixin):
    consumer_id: int
    provider_ids: List[int]
    interface_ids: List[int]
    service_definition_ids: List[int]


hello_auth_form = AuthorizationIntracloudForm(
        consumer_id=systems['consumer1'][1],
        provider_ids=[systems['producer1'][1]],
        interface_ids=[1],
        service_definition_ids=[hello_id],
)
echo_auth_form = AuthorizationIntracloudForm(
        consumer_id=systems['consumer1'][1],
        provider_ids=[systems['producer1'][1]],
        interface_ids=[1],
        service_definition_ids=[echo_id],
)

setup_client.consume_service(
        'mgmt_authorization_store',
        json=hello_auth_form.dto()
)
setup_client.consume_service(
        'mgmt_authorization_store',
        json=echo_auth_form.dto()
)

print('Local cloud setup finished!')
