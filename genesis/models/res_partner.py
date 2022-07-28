import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Contacts"

    employee_ids = fields.One2many(
        'hr.employee', 'address_home_id', string='Employees', groups="hr.group_hr_user",
        help="Related employees based on their private address")

    @api.constrains('employee_ids')
    def ensure_single_employee(self):
        for partner in self:
            if len(partner.employee_ids) > 1:
                raise UserError(_("Un contact ne peut être lié qu'à un seul employé."))

    def to_map(self):
       for partner in self:
            data = {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email if partner.email else "",
            }
            if len(partner.employee_ids) == 1:
                data['employee_id'] = partner.employee_ids[0].id
            else:
                data['employee_id'] = -1
            return data