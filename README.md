# Zabbix Client

A unified Python client for the Zabbix API with connection management and comprehensive operations support.

## Features

- **Context manager support** for automatic connection handling
- **Read operations** for monitoring and dashboards
- **Write operations** for configuration management
- **Comprehensive constants** as Enums for Zabbix API values
- **Type hints** throughout for better IDE support

## Installation

### From GitHub Packages

```bash
pip install zabbix-client --index-url https://ghcr.io/yourorg
```

### From Git

```bash
pip install git+https://github.com/yourorg/zabbix-client.git
```

### For Development

```bash
git clone https://github.com/yourorg/zabbix-client.git
cd zabbix-client
pip install -e ".[dev]"
```

## Configuration

The client can be configured via constructor arguments or environment variables:

| Parameter  | Environment Variable       | Description          |
|------------|---------------------------|----------------------|
| `url`      | `ZABBIX_INTERNAL_URL`     | Zabbix server URL    |
| `username` | `ZABBIX_SERVER_USER`      | Zabbix username      |
| `password` | `ZABBIX_SERVER_PASSWORD`  | Zabbix password      |

## Usage

### Basic Usage with Context Manager

```python
from zabbix_client import ZabbixClient

with ZabbixClient(url, username, password) as client:
    # Read operations
    hosts = client.get_hosts_by_hostgroup("my-group")
    problems = client.get_problems_by_severity([4, 5], ["1"])

    # Write operations
    client.create_hostgroup("new-group")
    template_id = client.get_template_id("my-template")
```

### Using Environment Variables

```python
import os
from zabbix_client import ZabbixClient

os.environ["ZABBIX_INTERNAL_URL"] = "http://zabbix.example.com"
os.environ["ZABBIX_SERVER_USER"] = "Admin"
os.environ["ZABBIX_SERVER_PASSWORD"] = "secret"

with ZabbixClient() as client:
    hosts = client.get_all_host_ids()
```

### Manual Connection Management

```python
from zabbix_client import ZabbixClient

client = ZabbixClient(url, username, password)
try:
    client.connect()
    hosts = client.get_hosts_by_hostgroup("production")
finally:
    client.disconnect()
```

## API Reference

### Template Group Operations

- `create_templategroup(name)` - Create a template group
- `get_templategroup_id(name)` - Get template group ID by name

### Host Group Operations

- `create_hostgroup(name)` - Create a host group
- `get_hostgroup_id(name)` - Get host group ID by name
- `propagate_hostgroup(hostgroup_id)` - Propagate host group permissions

### Host Operations

- `get_hosts_by_hostgroup(hostgroup_name)` - Get all hosts in a group
- `get_host_by_trigger_id(trigger_id)` - Get host info by trigger ID
- `get_all_host_ids()` - Get all visible host IDs

### Template Operations

- `get_template_id(name)` - Get template ID by name
- `get_templates_by_templategroup(templategroup_name)` - Get templates in a group
- `get_all_template_ids()` - Get all visible template IDs

### Item Operations

- `get_item_path(key)` - Get item path by key
- `get_items_by_host(host_id)` - Get items for a host
- `get_item_id_by_trigger_id(trigger_id)` - Get item ID by trigger ID

### Discovery Rule Operations

- `get_discovery_rule_id(name)` - Get discovery rule ID by name

### Problem Operations

- `get_problems_by_severity(severities, hostgroup_ids)` - Get problems by severity

### User Operations

- `get_user_by_username(username)` - Get user info by username

### Macro Operations

- `get_user_macro_value(host_id, macro)` - Get user macro value

## Constants

The package exports Zabbix constants as Enums:

```python
from zabbix_client.constants import (
    # Severity levels
    Severity,

    # Item types
    ItemType,

    # Preprocessing types
    PreprocessingType,

    # Value types
    ValueType,

    # Interface/Agent types
    InterfaceType,

    # Status
    Status,

    # Trigger priorities
    TriggerPriority,

    # User roles
    UserRole,

    # Inventory
    InventoryMode,
    InventoryField,
)

# Usage examples
item_type = ItemType.SCRIPT  # 21
priority = TriggerPriority.HIGH  # 4
status = Status.ENABLED  # 0

# Enums work as integers
assert ItemType.SCRIPT == 21

# Lookup by name
field = InventoryField["LOCATION"]  # InventoryField.LOCATION (24)
```

## Development

### Running Tests

```bash
pytest
```

### Running Linter

```bash
ruff check .
```

### Type Checking

```bash
mypy src/
```
