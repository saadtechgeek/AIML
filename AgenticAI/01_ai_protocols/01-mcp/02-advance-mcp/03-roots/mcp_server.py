from pathlib import Path
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from mcp.server.fastmcp import Context
from core.video_converter import VideoConverter
from core.utils import file_url_to_path

mcp = FastMCP("VidsMCP", log_level="ERROR")


# authorizing access
# ------------------
# Remember: the MCP SDK does not attempt to limit what files or folders your tools attempt to read! You must implement that check yourself.
# Consider implementing a function like is_path_allowed, which will decide whether a path is accessible by comparing it to the list of roots.
async def is_path_allowed(requested_path: Path, ctx: Context) -> bool:
    roots_result = await ctx.session.list_roots()
    client_roots = roots_result.roots

    if not requested_path.exists():
        return False

    if requested_path.is_file():
        requested_path = requested_path.parent

    for root in client_roots:
        root_path = file_url_to_path(root.uri)
        try:
            requested_path.relative_to(root_path)
            return True
        except ValueError:
            continue

    return False


@mcp.tool()
async def convert_video(
    input_path: str = Field(description="Path to the input MP4 file"),
    format: str = Field(description="Output format (e.g. 'mov')"),
    *,
    ctx: Context,
):
    """Convert an MP4 video file to another format using ffmpeg"""
    input_file = VideoConverter.validate_input(input_path)

    # Ensure the input file is contained in a root
    # authorizing access
    # ------------------
    # Once you've put an authorization function together - 
    # like is_path_allowed - use it throughout your tools to ensure the requested path is accessible.
    if not await is_path_allowed(input_file, ctx):
        raise ValueError(f"Access to path is not allowed: {input_path}")

    return await VideoConverter.convert(input_path, format)


# Using the roots
# ----------------
# On to the server. The server will use the roots in two scenarios:
# Whenever a tool attempts to access a file or folder
# When a LLM (like Claude) needs to resolve a file or folder to a full path.
# Think of when a user says 'read the todos.txt file' - Claude needs to figure out
# where the text file is, and might do so by looking at the list of roots
# To handle the second case, we can either define a tool that lists out the roots
# or inject them directly in a prompt.
@mcp.tool()
async def list_roots(ctx: Context):
    """
    List all directories that are accessible to this server.
    These are the root directories where files can be read from or written to.
    """
    roots_result = await ctx.session.list_roots()
    # accessing the root
    # ------------------
    # Roots are accessed by calling ctx.session.list_roots().
    # This sends a message back to the client, which causes it to run the root-listing callback.
    client_roots = roots_result.roots

    return [file_url_to_path(root.uri) for root in client_roots]


@mcp.tool()
async def read_dir(
    path: str = Field(description="Path to a directory to read"),
    *,
    ctx: Context,
):
    """Read directory contents. Path must be within one of the client's roots."""
    requested_path = Path(path).resolve()

    if not await is_path_allowed(requested_path, ctx):
        raise ValueError("Error: can only read directories within a root")

    return [entry.name for entry in requested_path.iterdir()]


if __name__ == "__main__":
    mcp.run(transport="stdio")
