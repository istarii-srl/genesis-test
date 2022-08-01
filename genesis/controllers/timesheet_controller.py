import json
import logging
from odoo import http
from odoo.http import request, Response
from ...token_auth.controllers.auth_controller import AuthController
from dateutil import parser
import datetime

_logger = logging.getLogger(__name__)


class TimesheetController(http.Controller):

    @http.route("/timesheet/get_month_timesheets_for/<int:employee_id>/<string:date_month>", type="http", auth="public", csrf=False, cors="*")
    def get_month_timesheets_for(self, employee_id, date_month):
        _logger.info("CONTROLLER TIMESHEET => get timesheets for employee_id and month")
        
        if AuthController.is_authorized(request):
            query = TimesheetController.get_base_query(employee_id, date_month)
            timesheet_ids = request.env['account.analytic.line'].sudo().search(query)
            return request.make_response(json.dumps({"data": [timesheet.to_map() for timesheet in timesheet_ids]}))

        return Response("Unauthorized", status_code=401)


    @http.route("/timesheet/save_provisional/<int:employee_id>/<string:date_month>", type="http", auth="public", csrf=False, cors="*")
    def save_provisional_for(self, employee_id, date_month):
        _logger.info("CONTROLLER TIMESHEET => set provisional for employee_id and month")
        
        if AuthController.is_authorized(request):
            query = TimesheetController.get_base_query(employee_id, date_month) + [('linked_provisional_id', '!=', False)]
            timesheet_ids = request.env['account.analytic.line'].sudo().search(query)
            for timesheet_id in timesheet_ids:
                request.env['genesis.provisional.line'].sudo().create({
                    'is_timesheet': True,
                    'date': timesheet_id.date,
                    'employee_id': timesheet_id.employee_id,
                    'user_id': timesheet_id.user_id,
                    'departement_id': timesheet_id.department_id,
                    'project_id': timesheet_id.project_id,
                    'task_id': timesheet_id.task_id,
                    'leave_id': timesheet_id.leave_id,
                    'unit_amount': timesheet_id.unit_amount,
                    'duration_unit_amount': timesheet_id.duration_unit_amount,
                    'unit_amount_validate': timesheet_id.unit_amount_validate,
                    'can_edit': False,
                })
            return request.make_response(json.dumps({"data": [timesheet.to_map() for timesheet in timesheet_ids]}))

        return Response("Unauthorized", status_code=401)

    @staticmethod
    def get_month(date_month):
        first_date = parser.parse(date_month).replace(day=1).date()
        last_date = ((first_date.replace(day=28) + datetime.timedelta(days=4)) - datetime.timedelta(days=1))
        return first_date, last_date

    @staticmethod
    def get_base_query(employee_id, date_month):
        first_date, last_date = TimesheetController.get_month(date_month)
        query = [('is_timesheet', '=', True), ('employee_id', '=', employee_id), ('date' ,'>=', first_date), ('date', '<=', last_date), ('unit_amount', '>', 0)]
        return query