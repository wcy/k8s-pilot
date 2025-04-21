import os

import yaml

from server.server import mcp


@mcp.tool()
def get_clusters():
    kubeconfig_path = os.path.expanduser("~/.kube/config")
    with open(kubeconfig_path, "r") as f:
        config_data = yaml.safe_load(f)

    current_context = config_data.get("current-context")
    contexts = config_data.get("contexts", [])

    return [{
        "name": ctx["name"],
        "cluster": ctx["context"].get("cluster"),
        "user": ctx["context"].get("user"),
        "current": ctx["name"] == current_context,
    } for ctx in contexts]

@mcp.tool()
def get_current_cluster():
    kubeconfig_path = os.path.expanduser("~/.kube/config")
    with open(kubeconfig_path, "r") as f:
        config_data = yaml.safe_load(f)

    current_context = config_data.get("current-context")
    contexts = config_data.get("contexts", [])

    for ctx in contexts:
        if ctx["name"] == current_context:
            return {
                "name": ctx["name"],
                "cluster": ctx["context"].get("cluster"),
                "user": ctx["context"].get("user"),
            }
    return None