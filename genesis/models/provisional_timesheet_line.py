from odoo import models, fields 


class ProvisionalTimesheetLine(models.Modal):
    _name = 'genesis.provisional.line'
    _inherit = 'account.analytic.line'

    original_id = fields.Many2one('account.analytic.line', string="The original line from which this provisional was created")