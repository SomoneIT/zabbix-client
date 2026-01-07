"""
Zabbix Constants and Enums

This module contains all Zabbix-related constants, including severity levels,
item types, preprocessing types, and other configuration values.
"""

# =============================================================================
# Zabbix Severity Levels
# =============================================================================

ZABBIX_SEVERITIES: dict[str, int] = {
    "FATAL": 5,
    "CRITICAL": 4,
    "WARNING": 3,
    "AVERAGE": 2,
    "INFORMATION": 1,
    "NOT_CLASSIFIED": 0,
}

# Valid trigger statuses for this application
VALID_TRIGGER_STATUSES: frozenset[str] = frozenset(("FATAL", "CRITICAL", "WARNING"))

# =============================================================================
# Zabbix Item Types
# =============================================================================

ITEM_TYPE_ZABBIX_AGENT: int = 0
ITEM_TYPE_ZABBIX_TRAPPER: int = 2
ITEM_TYPE_SIMPLE_CHECK: int = 3
ITEM_TYPE_ZABBIX_INTERNAL: int = 5
ITEM_TYPE_ZABBIX_AGENT_ACTIVE: int = 7
ITEM_TYPE_EXTERNAL_CHECK: int = 10
ITEM_TYPE_DATABASE_MONITOR: int = 11
ITEM_TYPE_IPMI_AGENT: int = 12
ITEM_TYPE_SSH_AGENT: int = 13
ITEM_TYPE_TELNET_AGENT: int = 14
ITEM_TYPE_CALCULATED: int = 15
ITEM_TYPE_JMX_AGENT: int = 16
ITEM_TYPE_SNMP_TRAP: int = 17
ITEM_TYPE_DEPENDENT: int = 18
ITEM_TYPE_HTTP_AGENT: int = 19
ITEM_TYPE_SNMP_AGENT_V3: int = 20
ITEM_TYPE_SCRIPT: int = 21

ITEM_TYPE_MAP: dict[str, int] = {
    "zabbix_agent": ITEM_TYPE_ZABBIX_AGENT,
    "trapper": ITEM_TYPE_ZABBIX_TRAPPER,
    "simple": ITEM_TYPE_SIMPLE_CHECK,
    "internal": ITEM_TYPE_ZABBIX_INTERNAL,
    "active": ITEM_TYPE_ZABBIX_AGENT_ACTIVE,
    "external": ITEM_TYPE_EXTERNAL_CHECK,
    "database": ITEM_TYPE_DATABASE_MONITOR,
    "ipmi": ITEM_TYPE_IPMI_AGENT,
    "ssh": ITEM_TYPE_SSH_AGENT,
    "telnet": ITEM_TYPE_TELNET_AGENT,
    "calculated": ITEM_TYPE_CALCULATED,
    "jmx": ITEM_TYPE_JMX_AGENT,
    "snmp_trap": ITEM_TYPE_SNMP_TRAP,
    "dependent": ITEM_TYPE_DEPENDENT,
    "http": ITEM_TYPE_HTTP_AGENT,
    "script": ITEM_TYPE_SCRIPT,
    "disabled": ITEM_TYPE_SCRIPT,  # Script type, but will be disabled
}

# =============================================================================
# Zabbix Preprocessing Types
# =============================================================================

PREPROCESSING_CUSTOM_MULTIPLIER: int = 1
PREPROCESSING_RIGHT_TRIM: int = 2
PREPROCESSING_LEFT_TRIM: int = 3
PREPROCESSING_TRIM: int = 4
PREPROCESSING_REGEX: int = 5
PREPROCESSING_BOOLEAN_TO_DECIMAL: int = 6
PREPROCESSING_OCTAL_TO_DECIMAL: int = 7
PREPROCESSING_HEX_TO_DECIMAL: int = 8
PREPROCESSING_SIMPLE_CHANGE: int = 9
PREPROCESSING_CHANGE_PER_SECOND: int = 10
PREPROCESSING_XML_XPATH: int = 11
PREPROCESSING_JSONPATH: int = 12
PREPROCESSING_IN_RANGE: int = 13
PREPROCESSING_MATCHES_REGEX: int = 14
PREPROCESSING_NOT_MATCHES_REGEX: int = 15
PREPROCESSING_CHECK_JSON: int = 16
PREPROCESSING_CHECK_XML: int = 17
PREPROCESSING_CHECK_REGEX: int = 18
PREPROCESSING_DISCARD_UNCHANGED: int = 19
PREPROCESSING_DISCARD_UNCHANGED_HEARTBEAT: int = 20
PREPROCESSING_JAVASCRIPT: int = 21
PREPROCESSING_PROMETHEUS_PATTERN: int = 22
PREPROCESSING_PROMETHEUS_TO_JSON: int = 23
PREPROCESSING_CSV_TO_JSON: int = 24
PREPROCESSING_STR_REPLACE: int = 25
PREPROCESSING_CHECK_NOT_SUPPORTED: int = 26
PREPROCESSING_XML_TO_JSON: int = 27
PREPROCESSING_SNMP_WALK_VALUE: int = 28
PREPROCESSING_SNMP_WALK_TO_JSON: int = 29

# =============================================================================
# Zabbix Value Types
# =============================================================================

VALUE_TYPE_FLOAT: int = 0
VALUE_TYPE_CHARACTER: int = 1
VALUE_TYPE_LOG: int = 2
VALUE_TYPE_UNSIGNED: int = 3
VALUE_TYPE_TEXT: int = 4

VALUE_TYPE_MAP: dict[str, int] = {
    "float": VALUE_TYPE_FLOAT,
    "character": VALUE_TYPE_CHARACTER,
    "log": VALUE_TYPE_LOG,
    "unsigned": VALUE_TYPE_UNSIGNED,
    "text": VALUE_TYPE_TEXT,
}

# =============================================================================
# Zabbix Agent/Interface Types
# =============================================================================

AGENT_TYPE_ZABBIX: int = 1
AGENT_TYPE_SNMP: int = 2
AGENT_TYPE_IPMI: int = 3
AGENT_TYPE_JMX: int = 4

INTERFACE_TYPE_MAP: dict[str, int] = {
    "zabbix": AGENT_TYPE_ZABBIX,
    "snmp": AGENT_TYPE_SNMP,
    "ipmi": AGENT_TYPE_IPMI,
    "jmx": AGENT_TYPE_JMX,
}

# =============================================================================
# Zabbix Host/Item Status
# =============================================================================

STATUS_ENABLED: int = 0
STATUS_DISABLED: int = 1

# =============================================================================
# Zabbix Trigger Priority
# =============================================================================

TRIGGER_PRIORITY_NOT_CLASSIFIED: int = 0
TRIGGER_PRIORITY_INFORMATION: int = 1
TRIGGER_PRIORITY_WARNING: int = 2
TRIGGER_PRIORITY_AVERAGE: int = 3
TRIGGER_PRIORITY_HIGH: int = 4
TRIGGER_PRIORITY_DISASTER: int = 5

# =============================================================================
# Zabbix User Roles
# =============================================================================

USER_ROLE_USER: int = 1
USER_ROLE_ADMIN: int = 2
USER_ROLE_SUPER_ADMIN: int = 3

# =============================================================================
# Zabbix Host Inventory Fields
# =============================================================================

INVENTORY_ALIAS: int = 4
INVENTORY_ASSET_TAG: int = 11
INVENTORY_CHASSIS: int = 28
INVENTORY_CONTACT: int = 23
INVENTORY_CONTRACT_NUMBER: int = 32
INVENTORY_DATE_HW_DECOMM: int = 47
INVENTORY_DATE_HW_EXPIRY: int = 46
INVENTORY_DATE_HW_INSTALL: int = 45
INVENTORY_DATE_HW_PURCHASE: int = 44
INVENTORY_DEPLOYMENT_STATUS: int = 34
INVENTORY_HARDWARE: int = 14
INVENTORY_HARDWARE_FULL: int = 15
INVENTORY_HOST_NETMASK: int = 39
INVENTORY_HOST_NETWORKS: int = 38
INVENTORY_HOST_ROUTER: int = 40
INVENTORY_HW_ARCH: int = 30
INVENTORY_INSTALLER_NAME: int = 33
INVENTORY_LOCATION: int = 24
INVENTORY_LOCATION_LAT: int = 25
INVENTORY_LOCATION_LON: int = 26
INVENTORY_MACADDRESS_A: int = 12
INVENTORY_MACADDRESS_B: int = 13
INVENTORY_MODEL: int = 29
INVENTORY_NAME: int = 3
INVENTORY_NOTES: int = 27
INVENTORY_OOB_IP: int = 41
INVENTORY_OOB_NETMASK: int = 42
INVENTORY_OOB_ROUTER: int = 43
INVENTORY_OS: int = 5
INVENTORY_OS_FULL: int = 6
INVENTORY_OS_SHORT: int = 7
INVENTORY_POC_1_CELL: int = 61
INVENTORY_POC_1_EMAIL: int = 58
INVENTORY_POC_1_NAME: int = 57
INVENTORY_POC_1_NOTES: int = 63
INVENTORY_POC_1_PHONE_A: int = 59
INVENTORY_POC_1_PHONE_B: int = 60
INVENTORY_POC_1_SCREEN: int = 62
INVENTORY_POC_2_CELL: int = 68
INVENTORY_POC_2_EMAIL: int = 65
INVENTORY_POC_2_NAME: int = 64
INVENTORY_POC_2_NOTES: int = 70
INVENTORY_POC_2_PHONE_A: int = 66
INVENTORY_POC_2_PHONE_B: int = 67
INVENTORY_POC_2_SCREEN: int = 69
INVENTORY_SERIALNO_A: int = 8
INVENTORY_SERIALNO_B: int = 9
INVENTORY_SITE_ADDRESS_A: int = 48
INVENTORY_SITE_ADDRESS_B: int = 49
INVENTORY_SITE_ADDRESS_C: int = 50
INVENTORY_SITE_CITY: int = 51
INVENTORY_SITE_COUNTRY: int = 53
INVENTORY_SITE_NOTES: int = 56
INVENTORY_SITE_RACK: int = 55
INVENTORY_SITE_STATE: int = 52
INVENTORY_SITE_ZIP: int = 54
INVENTORY_SOFTWARE: int = 16
INVENTORY_SOFTWARE_APP_A: int = 18
INVENTORY_SOFTWARE_APP_B: int = 19
INVENTORY_SOFTWARE_APP_C: int = 20
INVENTORY_SOFTWARE_APP_D: int = 21
INVENTORY_SOFTWARE_APP_E: int = 22
INVENTORY_SOFTWARE_FULL: int = 17
INVENTORY_TAG: int = 10
INVENTORY_TYPE: int = 1
INVENTORY_TYPE_FULL: int = 2
INVENTORY_URL_A: int = 35
INVENTORY_URL_B: int = 36
INVENTORY_URL_C: int = 37
INVENTORY_VENDOR: int = 31
