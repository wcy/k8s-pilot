from server.server import mcp  # noqa: F401

if __name__ == "__main__":
    mcp.run(transport='stdio')