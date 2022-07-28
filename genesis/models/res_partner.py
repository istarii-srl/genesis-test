import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Contacts"

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


    def action_create_employee(self):
        for partner_id in self: 
            data = {
                'name': partner_id.name,
                'address_home_id': partner_id.id,
                'company_id': self.env.company.id,
                'work_email': partner_id.email,
                'mobile_phone': partner_id.mobile,
                'work_phone': partner_id.phone,
                'image_1920': partner_id.image_1920,
            }
            employee = self.env['hr.employee'].create(data)