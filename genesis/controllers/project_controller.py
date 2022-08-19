import json
import logging
from odoo import http
from odoo.http import request, Response
from ...token_auth.controllers.auth_controller import AuthController

_logger = logging.getLogger(__name__)

class ProjectController(http.Controller):

    @http.route("/project/get_projects_for/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def get_active_project_for_user(self, employee_id):
        _logger.info("CONTROLLER PROJECT => get projects for employee_id")
        if AuthController.is_authorized(request):

            order_lines = request.env['sale.order.line'].sudo().search([('employee_ids', 'in', employee_id)])
            orders = list({line.order_id for line in order_lines})
            projects = set()
            for order in orders:
                projects |= set([project for project in order.project_ids if not project.stage_id.is_inactivity])
            return request.make_response(json.dumps({"data": [project.to_map() for project in projects]}))

        return Response("Unauthorized", status=401)
