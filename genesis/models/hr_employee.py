from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrEmployeePrivate(models.Model):
    _name = "hr.employee"


    @api.constrains('address_home_id')
    def ensure_single_contact(self):
        for employee in self:
            contacts = self.env['res.partner'].search([('employee_ids', 'in', employee.id)])
            if (len(contacts) > 1):
                raise UserError(_("Le contact sélectionné est déjà lié à un autre employé. Un contact ne peut être lié qu'à un seul employé."))