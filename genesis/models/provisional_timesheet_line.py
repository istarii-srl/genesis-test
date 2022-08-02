from odoo import models, fields 


class ProvisionalTimesheetLine(models.Model):
    _name = 'genesis.provisional.line'
    _inherit = 'account.analytic.line'
    _description = 'Timesheet prévisionelle'

    tag_ids = fields.Many2many('account.analytic.tag', 'account_analytic_line_tag_rel2', 'line_id', 'tag_id')

    original_id = fields.Many2one('account.analytic.line', string="The original line from which this provisional was created")