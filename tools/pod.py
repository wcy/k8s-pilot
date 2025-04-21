from typing import Optional, Dict, List

from core.context import use_current_context
from server.server import mcp
from kubernetes.client import CoreV1Api
from core.kubeconfig import get_api_clients


@mcp.tool()
@use_current_context
def pod_list(context_name: str, namespace: str):
    """
    List all pods in a given namespace.

    Args:
        context_name: The Kubernetes context name
        namespace: The Kubernetes namespace

    Returns:
        List of pod basic information
    """
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]
    pods = core_v1.list_namespaced_pod(namespace)
    result = [{"name": pod.metadata.name} for pod in pods.items]
    return result


@mcp.tool()
@use_current_context
def pod_detail(context_name: str, namespace: str, name: str):
    """
    Get details of a specific pod.

    Args:
        context_name: The Kubernetes context name
        namespace: The Kubernetes namespace
        name: The pod name

    Returns:
        Detailed information about the pod
    """
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]
    pod = core_v1.read_namespaced_pod(name, namespace)
    result = {
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "status": pod.status.phase,
        "containers": [{"name": c.name, "image": c.image} for c in pod.spec.containers],
    }
    return result


@mcp.tool()
@use_current_context
def pod_create(context_name: str, namespace: str, name: str, image: str,
               labels: Optional[Dict[str, str]] = None,
               command: Optional[List[str]] = None,
               args: Optional[List[str]] = None,
               env_vars: Optional[Dict[str, str]] = None):
    """
    Create a new pod in the specified namespace.

    Args:
        context_name: The Kubernetes context name
        namespace: The Kubernetes namespace
        name: The name for the new pod
        image: The container image to use
        labels: Optional dictionary of pod labels
        command: Optional command to run in the container
        args: Optional arguments for the command
        env_vars: Optional environment variables for the container

    Returns:
        Information about the created pod
    """
    from kubernetes.client import V1Pod, V1ObjectMeta, V1PodSpec, V1Container, V1EnvVar

    core_v1: CoreV1Api = get_api_clients(context_name)["core"]

    # Prepare environment variables if provided
    container_env = None
    if env_vars:
        container_env = [V1EnvVar(name=k, value=v) for k, v in env_vars.items()]

    # Create container
    container = V1Container(
        name=name,
        image=image,
        command=command,
        args=args,
        env=container_env
    )

    # Create pod spec
    pod_spec = V1PodSpec(containers=[container])

    # Create pod metadata
    pod_metadata = V1ObjectMeta(name=name, namespace=namespace, labels=labels)

    # Create pod
    pod = V1Pod(
        api_version="v1",
        kind="Pod",
        metadata=pod_metadata,
        spec=pod_spec
    )

    # Create the pod in Kubernetes
    created_pod = core_v1.create_namespaced_pod(namespace=namespace, body=pod)

    result = {
        "name": created_pod.metadata.name,
        "namespace": created_pod.metadata.namespace,
        "status": "Created",
    }
    return result


@mcp.tool()
@use_current_context
def pod_update(context_name: str, namespace: str, name: str,
               labels: Optional[Dict[str, str]] = None):
    """
    Update an existing pod's metadata (only labels can be updated for an existing pod).

    Args:
        context_name: The Kubernetes context name
        namespace: The Kubernetes namespace
        name: The pod name
        labels: New labels to apply to the pod

    Returns:
        Information about the updated pod
    """
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]

    # Get the current pod
    pod = core_v1.read_namespaced_pod(name=name, namespace=namespace)

    # Update pod labels if provided
    if labels:
        pod.metadata.labels = labels

    # Update the pod in Kubernetes
    updated_pod = core_v1.patch_namespaced_pod(
        name=name,
        namespace=namespace,
        body={"metadata": {"labels": labels}}
    )

    result = {
        "name": updated_pod.metadata.name,
        "namespace": updated_pod.metadata.namespace,
        "status": updated_pod.status.phase,
        "labels": updated_pod.metadata.labels,
    }
    return result


@mcp.tool()
@use_current_context
def pod_delete(context_name: str, namespace: str, name: str):
    """
    Delete a pod from the specified namespace.

    Args:
        context_name: The Kubernetes context name
        namespace: The Kubernetes namespace
        name: The pod name to delete

    Returns:
        Status of the deletion operation
    """
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]

    # Delete the pod
    api_response = core_v1.delete_namespaced_pod(
        name=name,
        namespace=namespace,
        body={}  # Default deletion options
    )

    result = {
        "name": name,
        "namespace": namespace,
        "status": "Deleted",
        "message": f"Pod {name} deleted successfully"
    }
    return result


@mcp.tool()
@use_current_context
def pod_logs(context_name: str, namespace: str, name: str, container: str = None,
             tail_lines: int = 100, previous: bool = False):
    """
    Get logs from a pod or a specific container within the pod.

    Args:
        context_name: The Kubernetes context name
        namespace: The Kubernetes namespace
        name: The pod name
        container: Optional container name (if pod has multiple containers)
        tail_lines: Number of lines to retrieve from the end of the logs
        previous: Whether to get logs from a previous instance of the container

    Returns:
        Pod logs
    """
    core_v1: CoreV1Api = get_api_clients(context_name)["core"]

    logs = core_v1.read_namespaced_pod_log(
        name=name,
        namespace=namespace,
        container=container,
        tail_lines=tail_lines,
        previous=previous
    )

    result = {
        "name": name,
        "namespace": namespace,
        "container": container,
        "logs": logs
    }
    return result
