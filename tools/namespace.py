import json
from kubernetes.client import CoreV1Api

from core.kubeconfig import get_api_clients
from server.server import mcp


@mcp.tool()
def list_namespaces(context_name: str):
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]
    namespaces = core_v1.list_namespace()
    result = [{"name": ns.metadata.name} for ns in namespaces.items]
    return json.dumps(result)
