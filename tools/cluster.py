import os

import yaml

from core.kubeconfig import get_kubeconfig
from server.server import mcp


@mcp.tool()
def get_clusters():
    config_data = get_kubeconfig()
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
    config_data = get_kubeconfig()
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

