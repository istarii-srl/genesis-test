import json
import logging
from odoo import http
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class ProjectController(http.Controller):

    @http.route("/projects/get_projects_for/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def get_active_project_for_user(self):
        
        return ""