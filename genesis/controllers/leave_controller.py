import json
import logging
from operator import le
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
                nb_of_days_allocated = allocation_id.max_leaves
                nb_days_taken = allocation_id.leaves_taken
                total_taken, total_allocated = allocations.get(leave_type, (0, 0))
                total_allocated += nb_of_days_allocated
                total_taken += nb_days_taken
                allocations[leave_type] = (total_taken, total_allocated)
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
            public_leaves = request.env["resource.calendar.leaves"].sudo().search([("year", ">=", current_year), ("resource_id", "=", False)])

            return request.make_response(json.dumps({"data": [leave.to_map() for leave in public_leaves]}))

        return Response("Unauthorized", status=401)


    @http.route("/leave/create/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def create_leaves(self, employee_id):
        _logger.info("CONTROLLER LEAVE => create")
        if AuthController.is_authorized(request):

            new_entries = json.loads(request.params['entries'])
            for new_entry in new_entries:
                self._create_leave(employee_id, new_entry)
            return request.make_response(json.dumps({"status": True})) 

        return Response("Unauthorized", status=401)

    def _create_leave(self, employee_id, data):
        leave = request.env['hr.leave'].sudo().create({
            'employee_id': employee_id,
            'holiday_status_id': data['leave']['type_id'],
            'date_from': parser.parse(data['date']).replace(hour=7),
            'date_to': parser.parse(data['date']).replace(hour=17),
            'state': 'validate',
        })
        return leave
    
    @http.route("/leave/update/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def update_leave(self, employee_id):
        _logger.info("CONTROLLER LEAVE => update")
        if AuthController.is_authorized(request):

            entry = json.loads(request.params['data'])
            self._delete_leave(entry['leave']['id'])
            self._create_leave(employee_id, entry)
            return request.make_response(json.dumps({"status": True})) 

        return Response("Unauthorized", status=401)


    @http.route("/leave/delete", type="http", auth="public", csrf=False, cors="*")
    def delete_leave(self):
        _logger.info("CONTROLLER LEAVE => delete")
        if AuthController.is_authorized(request):
            
            entry = json.loads(request.params['data'])
            self._delete_leave(entry['leave']['id'])
            return request.make_response(json.dumps({"status": True})) 

        return Response("Unauthorized", status=401)

    def _delete_leave(self, leave_id):
        leave = request.env['hr.leave'].sudo().browse(leave_id)
        if leave.state in ['confirm', 'validate', 'validate1']:
            leave.sudo().action_refuse()
        if leave.state == 'refuse':
            leave.sudo().action_draft()
        if leave.state == 'draft':
            leave.sudo().unlink()