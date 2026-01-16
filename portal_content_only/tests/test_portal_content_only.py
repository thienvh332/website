# Copyright 2026 Kencove (https://www.kencove.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPortalContentOnly(TransactionCase):
    """Test cases for portal content-only functionality."""

    def test_parse_content_only_truthy_values(self):
        """Test various truthy values for content_only parameter."""
        IrHttp = self.env["ir.http"]
        truthy_values = ["1", "true", "True", "TRUE"]
        for value in truthy_values:
            result = IrHttp._parse_content_only(value)
            self.assertTrue(result, f"Expected True for content_only={value}")

    def test_parse_content_only_falsy_values(self):
        """Test various falsy values for content_only parameter."""
        IrHttp = self.env["ir.http"]
        falsy_values = ["0", "false", "False", "FALSE", ""]
        for value in falsy_values:
            result = IrHttp._parse_content_only(value)
            self.assertFalse(result, f"Expected False for content_only={value}")

    def test_parse_content_only_none(self):
        """Test that None returns False."""
        IrHttp = self.env["ir.http"]
        result = IrHttp._parse_content_only(None)
        self.assertFalse(result)

    def test_excluded_path_prefixes(self):
        """Test that excluded paths are defined correctly."""
        IrHttp = self.env["ir.http"]
        expected_prefixes = (
            "/web",
            "/static",
            "/web/image",
            "/web/content",
            "/web/assets",
            "/website/image",
            "/sitemap",
            "/robots.txt",
            "/favicon",
            "/xmlrpc",
            "/jsonrpc",
        )
        self.assertEqual(IrHttp.EXCLUDED_PATH_PREFIXES, expected_prefixes)

    def test_res_config_settings_field(self):
        """Test that res.config.settings has the toggle button field."""
        settings = self.env["res.config.settings"].create({})
        self.assertTrue(hasattr(settings, "portal_content_only_toggle_enabled"))
