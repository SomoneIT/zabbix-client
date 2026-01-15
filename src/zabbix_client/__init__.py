"""
Zabbix Client Package

A unified Zabbix API client for connection management and operations.
"""

from zabbix_client import constants
from zabbix_client.client import ZabbixClient
from zabbix_client.exceptions import EntityAlreadyExistsError, ZabbixClientError

__version__ = "0.1.0"

__all__ = [
    # Main client
    "ZabbixClient",
    # Exceptions
    "ZabbixClientError",
    "EntityAlreadyExistsError",
    # Constants namespace
    "constants",
    # Version
    "__version__",
]
