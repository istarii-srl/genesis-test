import json
import logging
from odoo import http
from odoo.http import request, Response
from ...token_auth.controllers.auth_controller import AuthController
from dateutil import parser
import datetime

_logger = logging.getLogger(__name__)


class LeaveController(http.Controller):

    @http.route("/leave/get_all_leave_types", type="http", auth="public", csrf=False, cors="*")
    def get_all_leave_types(self):
        _logger.info("CONTROLLER LEAVE => get all leave types")
        if AuthController.is_authorized(request):

            leave_types = request.env['hr.leave.type'].sudo().search([])
            return request.make_response(json.dumps({"data": [leave_type.to_map() for leave_type in leave_types]}))

        return Response("Unauthorized", status_code=401)


    @http.route("/leave/create/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def create_leaves(self, employee_id):
        _logger.info("CONTROLLER LEAVE => create")
        if AuthController.is_authorized(request):

            new_entries = json.loads(request.params['entries'])
            for new_entry in new_entries:
                request.env['hr.leave'].sudo().create({
                    'employee_id': employee_id,
                    'holiday_status_id': new_entry['leave_id'],
                    'date_from': parser.parse(new_entry['date']).replace(hour=7),
                    'number_of_days': new_entry['duration'],
                    'state': 'validate',
                })
            return request.make_response(json.dumps({"status": True})) 

        return Response("Unauthorized", status_code=401)