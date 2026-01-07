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

INVENTORY: dict[str, int] = {
    "ALIAS": 4,
    "ASSET_TAG": 11,
    "CHASSIS": 28,
    "CONTACT": 23,
    "CONTRACT_NUMBER": 32,
    "DATE_HW_DECOMM": 47,
    "DATE_HW_EXPIRY": 46,
    "DATE_HW_INSTALL": 45,
    "DATE_HW_PURCHASE": 44,
    "DEPLOYMENT_STATUS": 34,
    "HARDWARE": 14,
    "HARDWARE_FULL": 15,
    "HOST_NETMASK": 39,
    "HOST_NETWORKS": 38,
    "HOST_ROUTER": 40,
    "HW_ARCH": 30,
    "INSTALLER_NAME": 33,
    "LOCATION": 24,
    "LOCATION_LAT": 25,
    "LOCATION_LON": 26,
    "MACADDRESS_A": 12,
    "MACADDRESS_B": 13,
    "MODEL": 29,
    "NAME": 3,
    "NOTES": 27,
    "OOB_IP": 41,
    "OOB_NETMASK": 42,
    "OOB_ROUTER": 43,
    "OS": 5,
    "OS_FULL": 6,
    "OS_SHORT": 7,
    "POC_1_CELL": 61,
    "POC_1_EMAIL": 58,
    "POC_1_NAME": 57,
    "POC_1_NOTES": 63,
    "POC_1_PHONE_A": 59,
    "POC_1_PHONE_B": 60,
    "POC_1_SCREEN": 62,
    "POC_2_CELL": 68,
    "POC_2_EMAIL": 65,
    "POC_2_NAME": 64,
    "POC_2_NOTES": 70,
    "POC_2_PHONE_A": 66,
    "POC_2_PHONE_B": 67,
    "POC_2_SCREEN": 69,
    "SERIALNO_A": 8,
    "SERIALNO_B": 9,
    "SITE_ADDRESS_A": 48,
    "SITE_ADDRESS_B": 49,
    "SITE_ADDRESS_C": 50,
    "SITE_CITY": 51,
    "SITE_COUNTRY": 53,
    "SITE_NOTES": 56,
    "SITE_RACK": 55,
    "SITE_STATE": 52,
    "SITE_ZIP": 54,
    "SOFTWARE": 16,
    "SOFTWARE_APP_A": 18,
    "SOFTWARE_APP_B": 19,
    "SOFTWARE_APP_C": 20,
    "SOFTWARE_APP_D": 21,
    "SOFTWARE_APP_E": 22,
    "SOFTWARE_FULL": 17,
    "TAG": 10,
    "TYPE": 1,
    "TYPE_FULL": 2,
    "URL_A": 35,
    "URL_B": 36,
    "URL_C": 37,
    "VENDOR": 31,
}

INVENTORY_MODE: dict[str, int] = {
    "DISABLED": -1,
    "MANUAL": 0,
    "AUTOMATIC": 1,
}
