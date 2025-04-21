from mcp.server.fastmcp import FastMCP

mcp = FastMCP("k8s-pilot")


# Tool/resource registration (required to trigger @mcp.tool/@mcp.resource)
def load_modules():
    import tools.cluster  # noqa: F401
    import tools.namespace  # noqa: F401
    import tools.pod  # noqa: F401
    import resources.contexts  # noqa: F401


load_modules()
