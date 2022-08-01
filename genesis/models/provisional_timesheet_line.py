from odoo import models, fields 


class ProvisionalTimesheetLine(models.Model):
    _name = 'genesis.provisional.line'
    _inherit = 'account.analytic.line'

    tag_ids = fields.Many2many('account.analytic.tag')

    original_id = fields.Many2one('account.analytic.line', string="The original line from which this provisional was created")