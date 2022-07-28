import logging
from odoo import models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Contacts"

    def to_map(self):
       for partner in self:
            data = {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email if partner.email else "",
            }
            if len(partner.employee_ids == 1):
                data['employee_id'] = partner.employee_ids[0]
            return data