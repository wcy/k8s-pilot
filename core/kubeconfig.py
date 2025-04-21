from kubernetes import client, config
from typing import Dict

_client_cache: Dict[str, Dict[str, any]] = {}

def get_api_clients(context_name: str) -> Dict[str, any]:
    if context_name not in _client_cache:
        configuration = client.Configuration()
        config.load_kube_config(context=context_name, client_configuration=configuration)
        api_client = client.ApiClient(configuration=configuration)
        _client_cache[context_name] = {
            "core": client.CoreV1Api(api_client),
            "apps": client.AppsV1Api(api_client),
            "batch": client.BatchV1Api(api_client),
        }
    return _client_cache[context_name]
