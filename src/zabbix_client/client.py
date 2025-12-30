"""
Zabbix Client Module

Unified wrapper around the Zabbix API for connection management and operations.
Combines read operations (monitoring/dashboard) and write operations (generator).
"""

import logging
import os
from typing import Any, cast

from zabbix_utils import ZabbixAPI
from zabbix_utils.exceptions import APIRequestError, ProcessingError

logger = logging.getLogger(__name__)


class ZabbixClient:
    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self.url: str = url or os.getenv("ZABBIX_INTERNAL_URL", "")
        if not self.url:
            raise ValueError("Zabbix URL is not set or empty.")

        self.user: str = username or os.getenv("ZABBIX_SERVER_USER", "")
        if not self.user:
            raise ValueError("Zabbix user is not set or empty.")

        self.password: str | None = password or os.getenv("ZABBIX_SERVER_PASSWORD")
        if not self.password:
            raise ValueError("Zabbix password is not set or empty.")

        self.client: ZabbixAPI | None = None
        self._connected: bool = False

    def __enter__(self) -> "ZabbixClient":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        self.disconnect()

    def connect(self) -> None:
        """Establish connection to Zabbix server."""
        if self._connected:
            return

        try:
            self.client = ZabbixAPI(url=self.url)
            if self.client and self.password:
                self.client.login(user=self.user, password=self.password)
                self._connected = True
                logger.info("Connected to Zabbix server at %s", self.url)
            else:
                raise ValueError(
                    "Invalid Zabbix configuration: missing password \
                    or client initialization failed"
                )
        except ProcessingError as e:
            logger.error(
                "Failed to connect to Zabbix server. \
                Server not running or not accessible: %s",
                e,
            )
            self._connected = False
            self.client = None
            raise ConnectionError(f"Server not accessible: {e}") from e
        except APIRequestError as e:
            self._connected = False
            self.client = None
            if "Incorrect user name or password" in str(e):
                logger.error(
                    "Failed to connect to Zabbix server.\
                    Incorrect user name or password"
                )
                raise PermissionError(f"Wrong credentials: {e}") from e
            raise
        except Exception:
            self._connected = False
            self.client = None
            raise

    def disconnect(self) -> None:
        """Disconnect from Zabbix server."""
        if self.client and self._connected:
            try:
                self.client.logout()
                logger.info("Disconnected from Zabbix server")
            except Exception as e:
                logger.warning("Error during logout: %s", e)
            finally:
                self._connected = False
                self.client = None

    def _ensure_connected(self) -> ZabbixAPI:
        """Ensure we have an active connection and return the client."""
        if not self._connected or not self.client:
            self.connect()
        if self.client is None:
            raise RuntimeError("Zabbix client connection could not be established.")
        return self.client

    def is_connected(self) -> bool:
        """Check if the client is currently connected."""
        return self._connected and self.client is not None

    # =========================================================================
    # Template Group Operations
    # =========================================================================

    def create_templategroup(self, name: str) -> dict[str, Any]:
        """Create a template group."""
        logger.info("Creating template group %s", name)
        client = self._ensure_connected()
        return cast(dict[str, Any], client.templategroup.create({"name": name}))  # type: ignore[attr-defined]

    def get_templategroup_id(self, name: str) -> str:
        """Get template group ID by name."""
        client = self._ensure_connected()
        result = client.templategroup.get(  # type: ignore[attr-defined]
            {"filter": {"name": name}, "output": ["groupid"]}
        )
        return cast(str, result[0]["groupid"])

    # =========================================================================
    # Host Group Operations
    # =========================================================================

    def create_hostgroup(self, name: str) -> dict[str, Any]:
        """Create a host group."""
        logger.info("Creating host group %s", name)
        client = self._ensure_connected()
        return cast(dict[str, Any], client.hostgroup.create({"name": name}))  # type: ignore[attr-defined]

    def get_hostgroup_id(self, name: str) -> str:
        """Get host group ID by name."""
        logger.info("Getting host group id %s", name)
        client = self._ensure_connected()
        result = client.hostgroup.get({"filter": {"name": name}, "output": ["groupid"]})  # type: ignore[attr-defined]
        return cast(str, result[0]["groupid"])

    def propagate_hostgroup(self, hostgroup_id: str) -> None:
        """Propagate host group permissions."""
        logger.info("Propagating hostgroup %s", hostgroup_id)
        client = self._ensure_connected()
        client.hostgroup.propagate(  # type: ignore[attr-defined]
            {
                "groups": [{"groupid": hostgroup_id}],
                "permissions": True,
                "tag_filters": True,
            }
        )

    # =========================================================================
    # Host Operations
    # =========================================================================

    def get_hosts_by_hostgroup(self, hostgroup_name: str) -> list[dict[str, Any]]:
        """Get all hosts in a host group with extended information."""
        client = self._ensure_connected()
        hostgroup_id = self.get_hostgroup_id(hostgroup_name)

        return cast(
            list[dict[str, Any]],
            client.host.get(  # type: ignore[attr-defined]
                {
                    "groupids": hostgroup_id,
                    "output": ["host", "hostid", "status"],
                    "selectTags": "extend",
                    "selectInheritedTags": "extend",
                    "selectParentTemplates": ["templateid"],
                    "selectInventory": ["location_lat", "location_lon"],
                }
            ),
        )

    def get_host_by_triggerid(self, triggerid: str) -> str | None:
        """Get host name by trigger ID."""
        client = self._ensure_connected()
        triggers = client.trigger.get(  # type: ignore[attr-defined]
            filter={"triggerid": triggerid},
            selectHosts=["hostid", "host"],
            output=["triggerid", "description"],
            selectTags="extend",
            selectInheritedTags="extend",
        )
        if not triggers:
            return None

        trigger = triggers[0]
        hosts = trigger.get("hosts") if isinstance(trigger, dict) else None
        if not isinstance(hosts, list) or not hosts:
            return None

        host_entry = hosts[0]
        if not isinstance(host_entry, dict) or "host" not in host_entry:
            return None

        return cast(str, host_entry["host"])

    def get_visible_hostids(self) -> list[str]:
        """Get all visible host IDs."""
        client = self._ensure_connected()
        hostids = client.host.get(output=["hostid"])  # type: ignore[attr-defined]
        return [host["hostid"] for host in hostids]

    # =========================================================================
    # Template Operations
    # =========================================================================

    def get_template_id(self, name: str) -> str:
        """Get template ID by name."""
        logger.info("Getting template id %s", name)
        client = self._ensure_connected()
        result = client.template.get(  # type: ignore[attr-defined]
            {"filter": {"name": name}, "output": ["templateid"]}
        )
        if not result:
            raise ValueError(f"Template not found: {name}")
        return cast(str, result[0]["templateid"])

    def get_templates_by_templategroup(
        self, templategroup_name: str
    ) -> list[dict[str, Any]]:
        """Get all templates in a template group with extended information."""
        client = self._ensure_connected()
        templategroup_id = self.get_templategroup_id(templategroup_name)

        return cast(
            list[dict[str, Any]],
            client.template.get(  # type: ignore[attr-defined]
                {
                    "groupids": templategroup_id,
                    "output": ["host", "templateid"],
                    "selectTags": "extend",
                    "selectInheritedTags": "extend",
                    "selectHosts": ["hostid"],
                }
            ),
        )

    def get_visible_templateids(self) -> list[str]:
        """Get all visible template IDs."""
        client = self._ensure_connected()
        templateids = client.template.get(output=["templateid"])  # type: ignore[attr-defined]
        return [template["templateid"] for template in templateids]

    # =========================================================================
    # Item Operations
    # =========================================================================

    def get_item_path(self, key: str) -> str:
        """Get the full path of an item by its key."""
        logger.info("Getting item with key %s", key)
        client = self._ensure_connected()
        items = client.item.get(  # type: ignore[attr-defined]
            {
                "search": {"key_": key},
                "output": ["key_"],
                "templated": "true",
                "selectHosts": ["host"],
            }
        )
        if not items:
            raise ValueError(f"Item not found for key: {key}")
        return f"/{items[0]['hosts'][0]['host']}/{items[0]['key_']}"

    def get_items_by_hosts(self, hostid: str) -> list[dict[str, Any]]:
        """Get all items for a host with extended information."""
        client = self._ensure_connected()
        return cast(
            list[dict[str, Any]],
            client.item.get(  # type: ignore[attr-defined]
                hostids=hostid,
                output=[
                    "itemid",
                    "hostid",
                    "value_type",
                    "lastvalue",
                    "status",
                    "state",
                ],
                selectTags="extend",
                selectTriggers=["value", "priority"],
            ),
        )

    def get_item_id_by_triggerid(self, triggerid: str) -> str | None:
        """Get item ID by trigger ID."""
        client = self._ensure_connected()
        item = client.item.get(  # type: ignore[attr-defined]
            triggerids=[triggerid],
            output=["itemid"],
        )
        # Validate response is a non-empty list with dict containing 'itemid' key
        if (
            isinstance(item, list)
            and len(item) > 0
            and isinstance(item[0], dict)
            and "itemid" in item[0]
        ):
            return cast(str, item[0]["itemid"])
        return None

    # =========================================================================
    # Discovery Rule Operations
    # =========================================================================

    def get_discovery_rule_id(self, name: str) -> str:
        """Get discovery rule ID by name."""
        client = self._ensure_connected()
        result = client.discoveryrule.get(  # type: ignore[attr-defined]
            {"output": ["itemid"], "filter": {"name": name}}
        )
        if not result:
            raise ValueError(f"Discovery rule not found: {name}")
        return cast(str, result[0]["itemid"])

    # =========================================================================
    # Problem Operations
    # =========================================================================

    def get_problems_with_severities(
        self, severities: list[int], groupids: list[str]
    ) -> list[dict[str, Any]]:
        """Get problems filtered by severities and group IDs."""
        client = self._ensure_connected()
        return cast(
            list[dict[str, Any]],
            client.problem.get(  # type: ignore[attr-defined]
                output=["eventid", "clock", "objectid", "severity", "name"],
                selectTags="extend",
                severities=severities,
                groupids=groupids,
                suppressed=False,
            ),
        )

    # =========================================================================
    # User Operations
    # =========================================================================

    def get_user_by_username(self, username: str) -> dict[str, Any] | None:
        """Get user information by username."""
        client = self._ensure_connected()
        user = client.user.get(  # type: ignore[attr-defined]
            filter={"username": username},
            output=["userid", "name", "surname", "username"],
            getAccess=True,
            selectRole=["type"],
        )
        if not user:
            return None
        return cast(dict[str, Any], user[0])

    # =========================================================================
    # Macro Operations
    # =========================================================================

    def get_user_macro_value(self, host_id: str, macro: str) -> str | None:
        """Get user macro value for a host."""
        client = self._ensure_connected()
        macros = client.usermacro.get(  # type: ignore[attr-defined]
            hostids=host_id,
            filter={"macro": macro},
            output=["value"],
        )
        # Validate response is a non-empty list with dict containing 'value' key
        if (
            isinstance(macros, list)
            and len(macros) > 0
            and isinstance(macros[0], dict)
            and "value" in macros[0]
        ):
            return cast(str, macros[0]["value"])
        return None
