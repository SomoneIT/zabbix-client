"""
Tests for ZabbixClient

These tests verify the client initialization and basic functionality.
Integration tests require a running Zabbix server.
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from zabbix_client import ZabbixClient


class TestZabbixClientInit:
    """Tests for ZabbixClient initialization."""

    def test_init_with_explicit_params(self) -> None:
        """Test client initialization with explicit parameters."""
        client = ZabbixClient(
            url="http://zabbix.example.com",
            username="admin",
            password="secret",
        )
        assert client.url == "http://zabbix.example.com"
        assert client.user == "admin"
        assert client.password == "secret"
        assert client.client is None
        assert client._connected is False

    def test_init_with_env_vars(self) -> None:
        """Test client initialization with environment variables."""
        with patch.dict(
            os.environ,
            {
                "ZABBIX_INTERNAL_URL": "http://env.zabbix.com",
                "ZABBIX_SERVER_USER": "env_user",
                "ZABBIX_SERVER_PASSWORD": "env_pass",
            },
        ):
            client = ZabbixClient()
            assert client.url == "http://env.zabbix.com"
            assert client.user == "env_user"
            assert client.password == "env_pass"

    def test_init_missing_url_raises_error(self) -> None:
        """Test that missing URL raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            # Clear relevant env vars
            os.environ.pop("ZABBIX_INTERNAL_URL", None)
            with pytest.raises(ValueError, match="Zabbix URL is not set"):
                ZabbixClient(url="", username="user", password="pass")

    def test_init_missing_user_raises_error(self) -> None:
        """Test that missing username raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("ZABBIX_SERVER_USER", None)
            with pytest.raises(ValueError, match="Zabbix user is not set"):
                ZabbixClient(url="http://example.com", username="", password="pass")

    def test_init_missing_password_raises_error(self) -> None:
        """Test that missing password raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("ZABBIX_SERVER_PASSWORD", None)
            with pytest.raises(ValueError, match="Zabbix password is not set"):
                ZabbixClient(url="http://example.com", username="user", password="")


class TestZabbixClientConnection:
    """Tests for ZabbixClient connection management."""

    def test_is_connected_initially_false(self) -> None:
        """Test that is_connected returns False before connecting."""
        client = ZabbixClient(
            url="http://example.com", username="user", password="pass"
        )
        assert client.is_connected() is False

    @patch("zabbix_client.client.ZabbixAPI")
    def test_connect_success(self, mock_api_class: MagicMock) -> None:
        """Test successful connection."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        client = ZabbixClient(
            url="http://example.com", username="user", password="pass"
        )
        client.connect()

        mock_api_class.assert_called_once_with(url="http://example.com")
        mock_api.login.assert_called_once_with(user="user", password="pass")
        assert client.is_connected() is True

    @patch("zabbix_client.client.ZabbixAPI")
    def test_connect_already_connected(self, mock_api_class: MagicMock) -> None:
        """Test that connect() is idempotent."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        client = ZabbixClient(
            url="http://example.com", username="user", password="pass"
        )
        client.connect()
        client.connect()  # Second call should be no-op

        # Should only be called once
        assert mock_api_class.call_count == 1

    @patch("zabbix_client.client.ZabbixAPI")
    def test_disconnect(self, mock_api_class: MagicMock) -> None:
        """Test disconnection."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        client = ZabbixClient(
            url="http://example.com", username="user", password="pass"
        )
        client.connect()
        client.disconnect()

        mock_api.logout.assert_called_once()
        assert client.is_connected() is False
        assert client.client is None

    @patch("zabbix_client.client.ZabbixAPI")
    def test_context_manager(self, mock_api_class: MagicMock) -> None:
        """Test context manager usage."""
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api

        with ZabbixClient(
            url="http://example.com", username="user", password="pass"
        ) as client:
            assert client.is_connected() is True

        mock_api.logout.assert_called_once()


class TestZabbixClientOperations:
    """Tests for ZabbixClient API operations."""

    @patch("zabbix_client.client.ZabbixAPI")
    def test_get_hostgroup_id(self, mock_api_class: MagicMock) -> None:
        """Test getting host group ID."""
        mock_api = MagicMock()
        mock_api.hostgroup.get.return_value = [{"groupid": "123"}]
        mock_api_class.return_value = mock_api

        with ZabbixClient(
            url="http://example.com", username="user", password="pass"
        ) as client:
            result = client.get_hostgroup_id("my-group")

        assert result == "123"
        mock_api.hostgroup.get.assert_called_once()

    @patch("zabbix_client.client.ZabbixAPI")
    def test_get_visible_hostids(self, mock_api_class: MagicMock) -> None:
        """Test getting visible host IDs."""
        mock_api = MagicMock()
        mock_api.host.get.return_value = [
            {"hostid": "1"},
            {"hostid": "2"},
            {"hostid": "3"},
        ]
        mock_api_class.return_value = mock_api

        with ZabbixClient(
            url="http://example.com", username="user", password="pass"
        ) as client:
            result = client.get_visible_hostids()

        assert result == ["1", "2", "3"]

    @patch("zabbix_client.client.ZabbixAPI")
    def test_get_user_macro_value_found(self, mock_api_class: MagicMock) -> None:
        """Test getting user macro value when found."""
        mock_api = MagicMock()
        mock_api.usermacro.get.return_value = [{"value": "macro_value"}]
        mock_api_class.return_value = mock_api

        with ZabbixClient(
            url="http://example.com", username="user", password="pass"
        ) as client:
            result = client.get_user_macro_value("123", "{$MY_MACRO}")

        assert result == "macro_value"

    @patch("zabbix_client.client.ZabbixAPI")
    def test_get_user_macro_value_not_found(self, mock_api_class: MagicMock) -> None:
        """Test getting user macro value when not found."""
        mock_api = MagicMock()
        mock_api.usermacro.get.return_value = []
        mock_api_class.return_value = mock_api

        with ZabbixClient(
            url="http://example.com", username="user", password="pass"
        ) as client:
            result = client.get_user_macro_value("123", "{$MY_MACRO}")

        assert result is None
