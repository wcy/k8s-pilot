import json
from kubernetes.client import CoreV1Api

from core.kubeconfig import get_api_clients
from server.server import mcp


@mcp.tool()
def list_nodes(context_name: str):
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]
    nodes = core_v1.list_node()
    result = [{"name": node.metadata.name} for node in nodes.items]
    return json.dumps(result)
