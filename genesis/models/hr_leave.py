from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import timedelta
import logging


_logger = logging.getLogger(__name__)

class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'
    _name = 'hr.leave'
    _description = 'hr.leave'

    def to_map(self):
        return {
            'id': self.id,
            'type': self.holiday_status_id.to_map()
        }