import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)
class AnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    linked_provisional_id = fields.Many2one('genesis.provisional.line', string="The provisional line created from this line")

    def to_map(self):
        for line in self:
            _logger.info(line);
            _logger.info("holiday => " + str(line.holiday_id));
            _logger.info("task => " + str(line.task_id))
            _logger.info("project => " + str(line.project_id))
            data = {
                'id': line.id,
                'date': line.date.strftime('%Y-%m-%d'),
                'duration': line._get_timesheet_time_day(),
            }
            if line.holiday_id:
                data['leave'] = line.holiday_id.to_map()
            elif line.task_id:
                data['task'] = line.task_id.to_map()
            else:
                data['project'] = line.project_id.to_map()
            return data