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
        self.url: str | None = url or os.getenv("ZABBIX_INTERNAL_URL", "")
        if not self.url:
            raise ValueError("Zabbix URL is not set or empty.")

        self.user: str | None = username or os.getenv("ZABBIX_SERVER_USER", "")
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
                    "Invalid Zabbix configuration: missing password "
                    "or client initialization failed"
                )
        except ProcessingError as e:
            logger.error(
                "Failed to connect to Zabbix server. "
                "Server not running or not accessible: %s",
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
                    "Failed to connect to Zabbix server. "
                    "Incorrect user name or password"
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
    # Templategroup Operations
    # =========================================================================

    def create_templategroup(self, name: str) -> dict[str, Any]:
        """Create a templategroup.

        Args:
            name: Name of the templategroup to create.

        Returns:
            API response containing the created templategroup info.
        """
        logger.info("Creating templategroup %s", name)
        client = self._ensure_connected()
        return cast(dict[str, Any], client.templategroup.create({"name": name}))  # type: ignore[attr-defined]

    def get_templategroup_id(self, name: str) -> str:
        """Get templategroup ID by name.

        Args:
            name: Name of the templategroup.

        Returns:
            The templategroup ID.

        Raises:
            ValueError: If the templategroup is not found.
        """
        client = self._ensure_connected()
        result = client.templategroup.get(  # type: ignore[attr-defined]
            {"filter": {"name": name}, "output": ["groupid"]}
        )
        if not result:
            raise ValueError(f"Templategroup not found: {name}")
        return cast(str, result[0]["groupid"])

    # =========================================================================
    # Hostgroup Operations
    # =========================================================================

    def create_hostgroup(self, name: str) -> dict[str, Any]:
        """Create a hostgroup.

        Args:
            name: Name of the hostgroup to create.

        Returns:
            API response containing the created hostgroup info.
        """
        logger.info("Creating hostgroup %s", name)
        client = self._ensure_connected()
        return cast(dict[str, Any], client.hostgroup.create({"name": name}))  # type: ignore[attr-defined]

    def get_hostgroup_id(self, name: str) -> str:
        """Get hostgroup ID by name.

        Args:
            name: Name of the hostgroup.

        Returns:
            The hostgroup ID.

        Raises:
            ValueError: If the hostgroup is not found.
        """
        logger.info("Getting hostgroup id %s", name)
        client = self._ensure_connected()
        result = client.hostgroup.get(  # type: ignore[attr-defined]
            {"filter": {"name": name}, "output": ["groupid"]}
        )
        if not result:
            raise ValueError(f"Hostgroup not found: {name}")
        return cast(str, result[0]["groupid"])

    def propagate_hostgroup(self, hostgroup_id: str) -> None:
        """Propagate hostgroup permissions.

        Args:
            hostgroup_id: ID of the hostgroup to propagate.
        """
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
        """Get all hosts in a hostgroup with extended information.

        Args:
            hostgroup_name: Name of the hostgroup.

        Returns:
            List of host dictionaries with extended information.

        Raises:
            ValueError: If the hostgroup is not found.
        """
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

    def get_host_by_trigger_id(self, trigger_id: str) -> dict[str, Any]:
        """Get host information by trigger ID.

        Args:
            trigger_id: ID of the trigger.

        Returns:
            Host dictionary containing hostid and host name.

        Raises:
            ValueError: If the trigger or associated host is not found.
        """
        client = self._ensure_connected()
        triggers = client.trigger.get(  # type: ignore[attr-defined]
            filter={"triggerid": trigger_id},
            selectHosts=["hostid", "host"],
            output=["triggerid", "description"],
            selectTags="extend",
            selectInheritedTags="extend",
        )
        if not triggers:
            raise ValueError(f"Trigger not found: {trigger_id}")

        trigger = triggers[0]
        hosts = trigger.get("hosts") if isinstance(trigger, dict) else None
        if not isinstance(hosts, list) or not hosts:
            raise ValueError(f"No host associated with trigger: {trigger_id}")

        host_entry = hosts[0]
        if not isinstance(host_entry, dict):
            raise ValueError(f"Invalid host data for trigger: {trigger_id}")

        return cast(dict[str, Any], host_entry)

    def get_all_host_ids(self) -> list[str]:
        """Get all visible host IDs.

        Returns:
            List of host IDs.
        """
        client = self._ensure_connected()
        hosts = client.host.get(output=["hostid"])  # type: ignore[attr-defined]
        return [host["hostid"] for host in hosts]

    # =========================================================================
    # Template Operations
    # =========================================================================

    def get_template_id(self, name: str) -> str:
        """Get template ID by name.

        Args:
            name: Name of the template.

        Returns:
            The template ID.

        Raises:
            ValueError: If the template is not found.
        """
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
        """Get all templates in a templategroup with extended information.

        Args:
            templategroup_name: Name of the templategroup.

        Returns:
            List of template dictionaries with extended information.

        Raises:
            ValueError: If the templategroup is not found.
        """
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

    def get_all_template_ids(self) -> list[str]:
        """Get all visible template IDs.

        Returns:
            List of template IDs.
        """
        client = self._ensure_connected()
        templates = client.template.get(output=["templateid"])  # type: ignore[attr-defined]
        return [template["templateid"] for template in templates]

    # =========================================================================
    # Item Operations
    # =========================================================================

    def get_item_path(self, key: str) -> str:
        """Get the full path of an item by its key.

        Args:
            key: The item key to search for.

        Returns:
            Full path in format /<host>/<key>.

        Raises:
            ValueError: If the item is not found.
        """
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

    def get_items_by_host(self, host_id: str) -> list[dict[str, Any]]:
        """Get all items for a host with extended information.

        Args:
            host_id: ID of the host.

        Returns:
            List of item dictionaries with extended information.
        """
        client = self._ensure_connected()
        return cast(
            list[dict[str, Any]],
            client.item.get(  # type: ignore[attr-defined]
                hostids=host_id,
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

    def get_item_id_by_trigger_id(self, trigger_id: str) -> str:
        """Get item ID by trigger ID.

        Args:
            trigger_id: ID of the trigger.

        Returns:
            The item ID.

        Raises:
            ValueError: If no item is associated with the trigger.
        """
        client = self._ensure_connected()
        items = client.item.get(  # type: ignore[attr-defined]
            triggerids=[trigger_id],
            output=["itemid"],
        )
        if not items:
            raise ValueError(f"No item found for trigger: {trigger_id}")
        return cast(str, items[0]["itemid"])

    # =========================================================================
    # Discovery Rule Operations
    # =========================================================================

    def get_discovery_rule_id(self, name: str) -> str:
        """Get discovery rule ID by name.

        Args:
            name: Name of the discovery rule.

        Returns:
            The discovery rule ID.

        Raises:
            ValueError: If the discovery rule is not found.
        """
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

    def get_problems_by_severity(
        self, severities: list[int], hostgroup_ids: list[str]
    ) -> list[dict[str, Any]]:
        """Get problems filtered by severities and hostgroup IDs.

        Args:
            severities: List of severity levels to filter by.
            hostgroup_ids: List of hostgroup IDs to filter by.

        Returns:
            List of problem dictionaries.
        """
        client = self._ensure_connected()
        return cast(
            list[dict[str, Any]],
            client.problem.get(  # type: ignore[attr-defined]
                output=["eventid", "clock", "objectid", "severity", "name"],
                selectTags="extend",
                severities=severities,
                groupids=hostgroup_ids,
                suppressed=False,
            ),
        )

    # =========================================================================
    # User Operations
    # =========================================================================

    def get_user_by_username(self, username: str) -> dict[str, Any]:
        """Get user information by username.

        Args:
            username: The username to search for.

        Returns:
            User dictionary with user information.

        Raises:
            ValueError: If the user is not found.
        """
        client = self._ensure_connected()
        users = client.user.get(  # type: ignore[attr-defined]
            filter={"username": username},
            output=["userid", "name", "surname", "username"],
            getAccess=True,
            selectRole=["type"],
        )
        if not users:
            raise ValueError(f"User not found: {username}")
        return cast(dict[str, Any], users[0])

    # =========================================================================
    # Macro Operations
    # =========================================================================

    def get_user_macro_value(self, host_id: str, macro: str) -> str:
        """Get user macro value for a host.

        Args:
            host_id: ID of the host.
            macro: The macro name (e.g., "{$MACRO_NAME}").

        Returns:
            The macro value.

        Raises:
            ValueError: If the macro is not found for the host.
        """
        client = self._ensure_connected()
        macros = client.usermacro.get(  # type: ignore[attr-defined]
            hostids=host_id,
            filter={"macro": macro},
            output=["value"],
        )
        if not macros:
            raise ValueError(f"Macro {macro} not found for host: {host_id}")
        return cast(str, macros[0]["value"])
