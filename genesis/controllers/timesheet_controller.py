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
            query = TimesheetController.get_base_query(employee_id, date_month) + [('linked_provisional_id', '=', False)]
            timesheet_ids = request.env['account.analytic.line'].sudo().search(query)
            for timesheet_id in timesheet_ids:
                provisional = request.env['genesis.provisional.line'].sudo().create({
                    'is_timesheet': True,
                    'date': timesheet_id.date,
                    'employee_id': timesheet_id.employee_id.id,
                    'user_id': timesheet_id.user_id.id,
                    'department_id': timesheet_id.department_id.id,
                    'project_id': timesheet_id.project_id.id,
                    'task_id': timesheet_id.task_id.id,
                    'holiday_id': timesheet_id.holiday_id.id,
                    'unit_amount': timesheet_id.unit_amount,
                    'duration_unit_amount': timesheet_id.duration_unit_amount,
                    'unit_amount_validate': timesheet_id.unit_amount_validate,
                    'can_edit': False,
                })
                timesheet_id.linked_provisional_id = provisional
            return request.make_response(json.dumps({"status": True}))

        return Response("Unauthorized", status_code=401)


    @http.route("/timesheet/create/<int:employee_id>", type="http", auth="public", csrf=False, cors="*")
    def create_timesheet_entry(self, employee_id):
        _logger.info("CONTROLLER TIMESHEET => create timesheet entry")

        if AuthController.is_authorized(request):
            new_entries = json.loads(request.params['entries'])
            for new_entry in new_entries:
                project_id = new_entry['project_id']
                employee = request.env['hr.employee'].sudo().browse(employee_id)
                user = request.env['res.user'].sudo().search([('partner_id', '=', employee.address_home_id.id)], limit=1)
                so_line = request.env['sale.order.line'].search([('project_id', '=', project_id), ('employee_id', '=', employee_id)], limit=1)
                vals = {
                    'is_timesheet': True,
                    'date': parser.parse(new_entry['date']).date(),
                    'employee_id': employee_id,
                    'user_id': user.id,
                    'department_id': employee.department_id.id,
                    'project_id': project_id,
                    'unit_amount': TimesheetController._convert_days_to_hours(new_entry['duration']),
                    'so_line': so_line.id,
                }
                if new_entry['task_id']:
                    vals['task_id'] = new_entry['task_id']
                new_entry = request.env['account.analytic.line'].sudo().create(vals)
            return request.make_response(json.dumps({'status': True}))

        return Response("Unauthorized", status_code=401)


    @staticmethod
    def _convert_days_to_hours(days):
        uom_hour = request.env.ref('uom.product_uom_hour')
        uom_day = request.env.ref('uom.product_uom_day')
        return uom_day._compute_quantity(days, uom_hour, raise_if_failure=False)

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