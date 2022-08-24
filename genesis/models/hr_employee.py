import logging
import datetime
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
    folder_id = fields.Many2one(string="Répertoire personnel", comodel_name="documents.folder")

    previsional_state = fields.Selection([('not_applicable', 'Dispensé(e)'), ('pending', 'En attente'), ('submitted', 'Validée')], string="Statut de la prévisionnelle", compute="_compute_previsional_state")

    @api.constrains('address_home_id')
    def ensure_single_contact(self):
        for employee in self:
            employee.check_one_employee()

    def check_one_employee(self):
        for employee in self:
            contact = self.env['res.partner'].search([('employee_ids', 'in', employee.id)], limit=1)
            if (contact and len(contact.employee_ids) > 1):
                raise UserError(_("Le contact sélectionné est déjà lié à un autre employé. Un contact ne peut être lié qu'à un seul employé."))

    def _compute_previsional_state(self):
        if self.department_id.use_previsional:
            today = datetime.date.today()
            current_month_first_date = today.replace(day=1)
            next_month = today.replace(day=28) + datetime.timedelta(days=4)
            current_month_last_date = next_month - datetime.timedelta(days=next_month.day)
            previsional_entries = self.env['genesis.provisional.line'].search([('date', '>=', current_month_first_date), ('date', '<=', current_month_last_date)])
            if len(previsional_entries > 0):
                self.previsional_state = 'submitted'
            else:
                self.previsional_state = 'pending'
        else:
            self.previsional_state = 'not_applicable'