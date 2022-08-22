import logging
from odoo import fields, api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'sale.order'


    def ensure_no_two_employee(self):
        for order in self:
            employees = {}
            for line in order.order_line:
                employees_for_line = { employee_id: 1 for employee_id in line.employee_ids.ids }
                employees = { employee_id: employees.get(employee_id, 0) + employees_for_line.get(employee_id, 0) for employee_id in employees.keys() | employees_for_line.keys() }
            if (sum(employees.values()) > len(employees)):
                raise UserError(_("Il ne peut pas y avoir un même employé sur plusieurs ligne de vente."))

    def write(self, vals):
        super(SaleOrder, self).write(vals)
        for order in self:
            order.ensure_no_two_employee()