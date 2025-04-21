from mcp.server.fastmcp import FastMCP

mcp = FastMCP("k8s-pilot")


# Tool/resource registration
import tools.cluster
import tools.namespace
import tools.pod
import resources.contexts