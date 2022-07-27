import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class MainController(http.Controller):

    @http.route("/lesson/get_by_id/<int:lesson_id>", type="http", auth="public", csrf=False, cors="*")
    def get_active_project_for_user(self):
        return ""