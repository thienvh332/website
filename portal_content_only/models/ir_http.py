# Copyright 2026 Kencove (https://www.kencove.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from werkzeug.urls import url_decode, url_encode, url_parse
from werkzeug.utils import redirect

from odoo import models
from odoo.http import request
from odoo.tools.misc import str2bool


class IrHttp(models.AbstractModel):
    """Auto-add content_only parameter to URLs when enabled in session."""

    _inherit = "ir.http"

    EXCLUDED_PATH_PREFIXES = (
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

    @classmethod
    def _dispatch(cls, endpoint):
        cls._sync_content_only_session()
        if cls._should_add_content_only(endpoint):
            return redirect(cls._build_content_only_url(), code=302)
        return super()._dispatch(endpoint)

    @classmethod
    def _handle_error(cls, exception):
        cls._sync_content_only_session()
        return super()._handle_error(exception)

    @classmethod
    def _build_content_only_url(cls):
        parsed = url_parse(request.httprequest.url)
        query_params = url_decode(parsed.query)
        query_params["content_only"] = "1" if cls._get_content_only_value() else "0"
        return parsed.replace(query=url_encode(query_params)).to_url()

    @classmethod
    def _should_add_content_only(cls, endpoint=None):
        if request.httprequest.method not in ("GET", "HEAD"):
            return False
        if "content_only" in request.httprequest.args:
            return False
        path = request.httprequest.path
        if any(path.startswith(prefix) for prefix in cls.EXCLUDED_PATH_PREFIXES):
            return False
        if endpoint and endpoint.routing.get("type") != "http":
            return False
        return cls._get_content_only_value()

    @classmethod
    def _sync_content_only_session(cls):
        if "content_only" in request.httprequest.args:
            request.session["portal_content_only"] = cls._parse_content_only(
                request.httprequest.args.get("content_only")
            )

    @classmethod
    def _get_content_only_value(cls):
        if "content_only" in request.httprequest.args:
            return cls._parse_content_only(request.httprequest.args.get("content_only"))
        return request.session.get("portal_content_only", False)

    @staticmethod
    def _parse_content_only(value):
        return bool(str2bool(value, default=False))
