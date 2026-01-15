# Copyright 2026 Kencove (https://www.kencove.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request
from odoo.tools.misc import str2bool

from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalContentOnly(CustomerPortal):
    """Add content_only flag to portal template values."""

    def _get_content_only(self):
        return str2bool(request.params.get("content_only"), default=False)

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        values["content_only"] = self._get_content_only()
        return values

    def _get_page_view_values(
        self, document, access_token, values, session_history, no_breadcrumbs, **kwargs
    ):
        values = super()._get_page_view_values(
            document, access_token, values, session_history, no_breadcrumbs, **kwargs
        )
        values.setdefault("content_only", self._get_content_only())
        return values
