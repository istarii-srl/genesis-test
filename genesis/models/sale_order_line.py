import logging
from odoo import fields, api, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    employee_ids = fields.Many2many('hr.employee', string="Employé(s)")

    # @api.constrains('employee_ids')
    def ensure_no_two_employee(self):
        for line in self:
            order_id = line.order_id
            employees = {}
            for lines in order_id.order_line:
                for line in lines:
                    employees_for_line = { employee_id: 1 for employee_id in line.employee_ids.ids }
                    _logger.info("#############")
                    _logger.info(employees_for_line)
                    employees = { employee_id: employees.get(employee_id, 0) + employees_for_line[employee_id] for employee_id in employees_for_line.keys() }
            _logger.info(employees)
            if (sum(employees.values()) > len(employees)):
                raise UserError(_("Il ne peut pas y avoir un même employé sur plusieurs ligne de vente."))

    def write(self, vals):
        super(SaleOrderLine, self).write(vals)
        for line in self:
            line.ensure_no_two_employee()

