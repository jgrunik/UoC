"""
This module defines the MCP server for the UoC project.
"""
from fastmcp import FastMCP

from src.uoc_scraper import UoCData

mcp = FastMCP()

@mcp.tool()
def get_unit_data(unit_code: str) -> dict:
    """Scrapes and returns all data for a given Unit of Competency."""
    try:
        scraper = UoCData(unit_code)
        return scraper.extract_all()
    except ValueError as e:
        # It's better to let the server handle exceptions.
        # The client will receive a proper error response.
        raise
    except Exception as e:
        raise

@mcp.tool()
def validate_unit_code(unit_code: str) -> bool:
    """Validates the format of a Unit of Competency code."""
    return UoCData.validate_unit_code(unit_code)

if __name__ == "__main__":
    mcp.run()
