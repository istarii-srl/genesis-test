from odoo import models, api, fields

class Meeting(models.Model):
    _name = 'calendar.event'
    _inherit = 'calendar.event'

    name = fields.Char('Coucou hibou', required=True)

    #! copy paste ovveride to add sudo because of rights problems
    @api.model_create_multi
    def create(self, vals_list):
        return super(Meeting, self).sudo().create(vals_list)