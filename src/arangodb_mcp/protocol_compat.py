"""MCP protocol-version support check for the official MCP Python SDK.

MCP SDK 1.x advertised only up to 2025-11-25, so this module used to patch the
SDK's version lists to negotiate the 2026-07-28 wire revision. SDK 2.x supports
2026-07-28 natively (``mcp.types.version.SUPPORTED_PROTOCOL_VERSIONS``, and it is
``LATEST_PROTOCOL_VERSION``), and its version lists are immutable tuples, so no
bridge is applied any more. The check remains so a future SDK that dropped the
revision would fail at startup instead of silently downgrading.
"""

from __future__ import annotations

from mcp.types import version as sdk_version

MCP_2026_VERSION = "2026-07-28"
SDK_NATIVE_LATEST_VERSION = sdk_version.LATEST_PROTOCOL_VERSION
COMPATIBILITY_SUNSET = "2027-02-01"


def enable_mcp_2026_negotiation() -> bool:
    """Confirm native 2026-07-28 support; return whether a bridge was necessary.

    Always ``False`` on SDK 2.x. Raises if the SDK does not support the revision,
    because the immutable version tuples can no longer be patched.
    """
    if MCP_2026_VERSION not in sdk_version.SUPPORTED_PROTOCOL_VERSIONS:
        raise RuntimeError(
            f"The installed MCP SDK does not support protocol {MCP_2026_VERSION}; "
            f"it supports {sdk_version.SUPPORTED_PROTOCOL_VERSIONS}."
        )
    return False
