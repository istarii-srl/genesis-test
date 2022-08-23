import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class HrEmployeePrivate(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    address_home_id = fields.Many2one(
        'res.partner', 'Contact lié', help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    folder_id = fields.Many2one(string="Répertoire des documents", comodel_name="documents.folder")

    @api.constrains('address_home_id')
    def ensure_single_contact(self):
        for employee in self:
            employee.check_one_employee()

    def check_one_employee(self):
        for employee in self:
            contact = self.env['res.partner'].search([('employee_ids', 'in', employee.id)], limit=1)
            if (contact and len(contact.employee_ids) > 1):
                raise UserError(_("Le contact sélectionné est déjà lié à un autre employé. Un contact ne peut être lié qu'à un seul employé."))