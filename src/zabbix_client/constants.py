"""
Zabbix Constants

This module contains all Zabbix-related constants as enums.
"""

from enum import IntEnum


class Severity(IntEnum):
    """Zabbix trigger severity levels."""

    NOT_CLASSIFIED = 0
    INFORMATION = 1
    AVERAGE = 2
    WARNING = 3
    CRITICAL = 4
    FATAL = 5


class ItemType(IntEnum):
    """Zabbix item types."""

    ZABBIX_AGENT = 0
    ZABBIX_TRAPPER = 2
    SIMPLE_CHECK = 3
    ZABBIX_INTERNAL = 5
    ZABBIX_AGENT_ACTIVE = 7
    EXTERNAL_CHECK = 10
    DATABASE_MONITOR = 11
    IPMI_AGENT = 12
    SSH_AGENT = 13
    TELNET_AGENT = 14
    CALCULATED = 15
    JMX_AGENT = 16
    SNMP_TRAP = 17
    DEPENDENT = 18
    HTTP_AGENT = 19
    SNMP_AGENT_V3 = 20
    SCRIPT = 21


class PreprocessingType(IntEnum):
    """Zabbix preprocessing types."""

    CUSTOM_MULTIPLIER = 1
    RIGHT_TRIM = 2
    LEFT_TRIM = 3
    TRIM = 4
    REGEX = 5
    BOOLEAN_TO_DECIMAL = 6
    OCTAL_TO_DECIMAL = 7
    HEX_TO_DECIMAL = 8
    SIMPLE_CHANGE = 9
    CHANGE_PER_SECOND = 10
    XML_XPATH = 11
    JSONPATH = 12
    IN_RANGE = 13
    MATCHES_REGEX = 14
    NOT_MATCHES_REGEX = 15
    CHECK_JSON = 16
    CHECK_XML = 17
    CHECK_REGEX = 18
    DISCARD_UNCHANGED = 19
    DISCARD_UNCHANGED_HEARTBEAT = 20
    JAVASCRIPT = 21
    PROMETHEUS_PATTERN = 22
    PROMETHEUS_TO_JSON = 23
    CSV_TO_JSON = 24
    STR_REPLACE = 25
    CHECK_NOT_SUPPORTED = 26
    XML_TO_JSON = 27
    SNMP_WALK_VALUE = 28
    SNMP_WALK_TO_JSON = 29


class ValueType(IntEnum):
    """Zabbix value types."""

    FLOAT = 0
    CHARACTER = 1
    LOG = 2
    UNSIGNED = 3
    TEXT = 4


class InterfaceType(IntEnum):
    """Zabbix interface/agent types."""

    ZABBIX = 1
    SNMP = 2
    IPMI = 3
    JMX = 4


class Status(IntEnum):
    """Zabbix host/item status."""

    ENABLED = 0
    DISABLED = 1


class TriggerPriority(IntEnum):
    """Zabbix trigger priority levels."""

    NOT_CLASSIFIED = 0
    INFORMATION = 1
    WARNING = 2
    AVERAGE = 3
    HIGH = 4
    DISASTER = 5


class UserRole(IntEnum):
    """Zabbix user roles."""

    USER = 1
    ADMIN = 2
    SUPER_ADMIN = 3


class InventoryMode(IntEnum):
    """Zabbix inventory mode."""

    DISABLED = -1
    MANUAL = 0
    AUTOMATIC = 1


class InventoryField(IntEnum):
    """Zabbix host inventory fields."""

    TYPE = 1
    TYPE_FULL = 2
    NAME = 3
    ALIAS = 4
    OS = 5
    OS_FULL = 6
    OS_SHORT = 7
    SERIALNO_A = 8
    SERIALNO_B = 9
    TAG = 10
    ASSET_TAG = 11
    MACADDRESS_A = 12
    MACADDRESS_B = 13
    HARDWARE = 14
    HARDWARE_FULL = 15
    SOFTWARE = 16
    SOFTWARE_FULL = 17
    SOFTWARE_APP_A = 18
    SOFTWARE_APP_B = 19
    SOFTWARE_APP_C = 20
    SOFTWARE_APP_D = 21
    SOFTWARE_APP_E = 22
    CONTACT = 23
    LOCATION = 24
    LOCATION_LAT = 25
    LOCATION_LON = 26
    NOTES = 27
    CHASSIS = 28
    MODEL = 29
    HW_ARCH = 30
    VENDOR = 31
    CONTRACT_NUMBER = 32
    INSTALLER_NAME = 33
    DEPLOYMENT_STATUS = 34
    URL_A = 35
    URL_B = 36
    URL_C = 37
    HOST_NETWORKS = 38
    HOST_NETMASK = 39
    HOST_ROUTER = 40
    OOB_IP = 41
    OOB_NETMASK = 42
    OOB_ROUTER = 43
    DATE_HW_PURCHASE = 44
    DATE_HW_INSTALL = 45
    DATE_HW_EXPIRY = 46
    DATE_HW_DECOMM = 47
    SITE_ADDRESS_A = 48
    SITE_ADDRESS_B = 49
    SITE_ADDRESS_C = 50
    SITE_CITY = 51
    SITE_STATE = 52
    SITE_COUNTRY = 53
    SITE_ZIP = 54
    SITE_RACK = 55
    SITE_NOTES = 56
    POC_1_NAME = 57
    POC_1_EMAIL = 58
    POC_1_PHONE_A = 59
    POC_1_PHONE_B = 60
    POC_1_CELL = 61
    POC_1_SCREEN = 62
    POC_1_NOTES = 63
    POC_2_NAME = 64
    POC_2_EMAIL = 65
    POC_2_PHONE_A = 66
    POC_2_PHONE_B = 67
    POC_2_CELL = 68
    POC_2_SCREEN = 69
    POC_2_NOTES = 70
