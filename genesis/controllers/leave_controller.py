import json
import logging
from odoo import http
from odoo.http import request, Response
from odoo.tools import date_utils
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

        return Response("Unauthorized", status=401)


    @http.route("/leave/get_allocations/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def get_allocations(self, employee_id):
        _logger.info("CONTROLLER LEAVE => get leave allocation")
        if AuthController.is_authorized(request):

            allocation_ids = request.env['hr.leave.allocation'].sudo().search([('employee_id', '=', employee_id), ('holiday_status_id.active', '=', True)])
            allocations = {}
            for allocation_id in allocation_ids:
                leave_type = allocation_id.holiday_status_id
                nb_of_days_allocated = allocation_id.number_of_days
                nb_days_taken = sum(taken_leave.number_of_days for taken_leave in allocation_id.taken_leave_ids\
                    if taken_leave.state == 'validate')
                
                total_taken, total_allocated = allocations.get(leave_type, (0, 0))
                total_allocated += nb_of_days_allocated
                total_taken += nb_days_taken
                allocations[leave_type] = allocations[leave_type] = (total_taken, total_allocated)
            data = []
            for leave_type in allocations.keys():
                taken, allocated = allocations[leave_type]
                data.append({'leave': leave_type.to_map(), 'taken': taken, 'allocated': allocated})
            return request.make_response(json.dumps({"data": data}))

        return Response("Unauthorized", status=401)


    @http.route("/leave/get_public", type="http", auth="public", csrf=False, cors="*")
    def get_public_leaves(self):
        _logger.info("CONTROLLER LEAVE => get leave allocation")
        if AuthController.is_authorized(request):
            current_year = datetime.datetime.today().year;
            first_day_current_year = datetime.datetime(current_year, 1, 1)
            _logger.info(current_year)
            public_leaves = request.env["resource.calendar.leaves"].sudo().search([("date_from", ">=", first_day_current_year), ("resource_id", "=", False)])
            for leave in public_leaves:
                _logger.info(leave.date_from)
            return request.make_response(json.dumps({"data": [{
                "id": leave.id,
                "name": leave.name,
                "date_from": date_utils.json_default(leave.date_from),
                "date_to": date_utils.json_default(leave.date_to),
            } for leave in public_leaves]}))

        return Response("Unauthorized", status=401)


    @http.route("/leave/create/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def create_leaves(self, employee_id):
        _logger.info("CONTROLLER LEAVE => create")
        if AuthController.is_authorized(request):

            new_entries = json.loads(request.params['entries'])
            for new_entry in new_entries:
                _logger.info(new_entry)
                request.env['hr.leave'].sudo().create({
                    'employee_id': employee_id,
                    'holiday_status_id': new_entry['leave']['type_id'],
                    'date_from': parser.parse(new_entry['date']).replace(hour=7),
                    'date_to': parser.parse(new_entry['date']).replace(hour=17),
                    'state': 'validate',
                })
            return request.make_response(json.dumps({"status": True})) 

        return Response("Unauthorized", status=401)