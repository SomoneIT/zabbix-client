class ZabbixClientError(Exception):
    """Base exception for zabbix_client."""


class EntityAlreadyExistsError(ZabbixClientError):
    """Raised when trying to create an entity that already exists."""

    def __init__(self, entity_type: str, entity_name: str):
        self.entity_type = entity_type
        self.entity_name = entity_name
        super().__init__(f"{entity_type} already exists: {entity_name}")
