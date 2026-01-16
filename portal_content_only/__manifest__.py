# Copyright 2026 Kencove (https://www.kencove.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Portal Content Only",
    "version": "16.0.1.1.0",
    "summary": "Hide header/footer on portal pages with content_only parameter",
    "category": "Website",
    "author": "Kencove, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["portal", "web", "website"],
    "data": [
        "data/ir_config_parameter_data.xml",
        "views/portal_templates.xml",
        "views/web_templates.xml",
        "views/toggle_templates.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "portal_content_only/static/src/css/content_only_toggle.css",
        ],
    },
    "installable": True,
    "application": False,
}
