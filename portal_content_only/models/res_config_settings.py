# Copyright 2026 Kencove (https://www.kencove.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    portal_content_only_toggle_enabled = fields.Boolean(
        string="Show Content Only Toggle",
        help="""Display the toggle button that allows users to hide/show
        header and footer on portal pages""",
        default=False,
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        param = self.env["ir.config_parameter"].sudo()
        res["portal_content_only_toggle_enabled"] = (
            param.get_param("portal_content_only.toggle_enabled", "False").lower()
            == "true"
        )
        return res

    def set_values(self):
        res = super().set_values()
        param = self.env["ir.config_parameter"].sudo()
        param.set_param(
            "portal_content_only.toggle_enabled",
            str(self.portal_content_only_toggle_enabled),
        )
        return res
