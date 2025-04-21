from server.server import mcp


@mcp.tool()
def pod_list(context_name: str, namespace: str):
    """
    List all pods in a given namespace.
    """
    from kubernetes.client import CoreV1Api
    from core.kubeconfig import get_api_clients

    core_v1: CoreV1Api = get_api_clients(context_name)["core"]
    pods = core_v1.list_namespaced_pod(namespace)
    result = [{"name": pod.metadata.name} for pod in pods.items]
    return result