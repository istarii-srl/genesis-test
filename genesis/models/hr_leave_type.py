import logging


from odoo import models, fields
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HolidaysType(models.Model):
    _name = "hr.leave.type"
    _inherit = "hr.leave.type"

    internal_code = fields.Char('Code')

    def to_map(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.internal_code if self.internal_code else '',
        }