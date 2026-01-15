# Copyright 2026 Kencove (https://www.kencove.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestIrHttpContentOnly(TransactionCase):
    """Test cases for ir.http content_only methods with mocked request."""

    def _create_mock_request(self, path="/my", args=None, method="GET", session=None):
        """Helper to create a mock request object."""
        mock_request = MagicMock()
        mock_request.httprequest.path = path
        mock_request.httprequest.args = args or {}
        mock_request.httprequest.method = method
        mock_request.httprequest.url = f"http://localhost{path}"  # noqa: E231
        mock_request.session = session if session is not None else {}
        return mock_request

    def test_should_add_content_only_with_session(self):
        """Test _should_add_content_only returns True when session has content_only."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my/orders",
            args={},
            session={"portal_content_only": True},
        )
        mock_endpoint = MagicMock()
        mock_endpoint.routing = {"type": "http"}

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._should_add_content_only(mock_endpoint)
            self.assertTrue(result)

    def test_should_add_content_only_excluded_path(self):
        """Test _should_add_content_only returns False for excluded paths."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/web/login",
            args={},
            session={"portal_content_only": True},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._should_add_content_only(None)
            self.assertFalse(result)

    def test_should_add_content_only_already_has_param(self):
        """Test _should_add_content_only returns False when param already in URL."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={"content_only": "1"},
            session={"portal_content_only": True},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._should_add_content_only(None)
            self.assertFalse(result)

    def test_should_add_content_only_post_request(self):
        """Test _should_add_content_only returns False for POST requests."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={},
            method="POST",
            session={"portal_content_only": True},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._should_add_content_only(None)
            self.assertFalse(result)

    def test_sync_content_only_session_enable(self):
        """Test _sync_content_only_session stores True in session."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={"content_only": "1"},
            session={},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            IrHttp._sync_content_only_session()
            self.assertTrue(mock_request.session.get("portal_content_only"))

    def test_sync_content_only_session_disable(self):
        """Test _sync_content_only_session stores False in session."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={"content_only": "0"},
            session={"portal_content_only": True},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            IrHttp._sync_content_only_session()
            self.assertFalse(mock_request.session.get("portal_content_only"))

    def test_get_content_only_value_from_args(self):
        """Test _get_content_only_value reads from request args first."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={"content_only": "1"},
            session={"portal_content_only": False},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._get_content_only_value()
            self.assertTrue(result)

    def test_get_content_only_value_from_session(self):
        """Test _get_content_only_value falls back to session."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={},
            session={"portal_content_only": True},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._get_content_only_value()
            self.assertTrue(result)

    def test_get_content_only_value_default(self):
        """Test _get_content_only_value returns False by default."""
        IrHttp = self.env["ir.http"]
        mock_request = self._create_mock_request(
            path="/my",
            args={},
            session={},
        )

        with patch(
            "odoo.addons.portal_content_only.models.ir_http.request", mock_request
        ):
            result = IrHttp._get_content_only_value()
            self.assertFalse(result)
