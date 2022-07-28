import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"


    @api.constrains('address_home_id')
    def ensure_single_contact(self):
        _logger.info("*********")
        for employee in self:
            employee.check_one_employee(1)

    @api.onchange('address_home_id')
    def on_address_change(self):
        _logger.info("#########")
        for employee in self:
            employee.check_one_employee(0)

    def check_one_employee(self, minimum):
        for employee in self:
            contact = self.env['res.partner'].search([('employee_ids', 'in', employee.id)], limit=1)
            if (contact and len(contact.employee_ids) > minimum):
                raise UserError(_("Le contact sélectionné est déjà lié à un autre employé. Un contact ne peut être lié qu'à un seul employé."))