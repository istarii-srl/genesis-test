from odoo import _, api, fields, models

import logging


_logger = logging.getLogger(__name__)

class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'
    _name = 'hr.leave'
    _description = 'hr.leave'

    def action_validate(self):
        return super(HolidaysRequest, self).sudo().action_validate()
    