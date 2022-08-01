from odoo import models, fields
class AnalyticLine(models.Model):
    
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    linked_provisional_id = fields.Many2one('genesis.provisional.line', string="The provisional line created from this line")

    def to_map(self):
        data = {
            'id': self.id,
            'date': self.date,
            'duration': self.duration_unit,
        }
        if self.holiday_id:
            data['leave'] = self.leave_id.holiday_status_id.to_map()
        elif self.project_id:
            data['project'] = self.project_id.to_map()
        elif self.task_id:
            data['task'] = self.task_id.to_map()
        
        return data