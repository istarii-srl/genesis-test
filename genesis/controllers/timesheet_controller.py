import json
import logging
from odoo import http
from odoo.http import request, Response
from ...token_auth.controllers.auth_controller import AuthController
from dateutil import parser
import datetime

_logger = logging.getLogger(__name__)


class TimesheetController(http.Controller):

    @http.route("/projects/get_month_timesheets_for/<int:employee_id>/<string:date_month>", type="http", auth="public", csrf=False, cors="*")
    def get_month_timesheets_for(self, employee_id, date_month):
        _logger.info("CONTROLLER TIMESHEET => get timesheets for employee_id and month")
        
        if AuthController.is_authorized(request):
            first_date = parser.parse(date_month).replace(day=1).date()
            last_date = ((first_date.replace(day=28) + datetime.timedelta(days=4)) - datetime.timedelta(days=1)).date()
            query = [('is_timesheet', '=', True), ('employee_id', '=', employee_id), ('date' ,'>=', first_date), ('date', '<=', last_date)]
            timesheet_ids = request.env['account.analytic.line'].sudo().search(query)
            return request.make_response(json.dumps({"data": [timesheet.to_map() for timesheet in timesheet_ids]}))

        return Response("Unauthorized", status_code=401)