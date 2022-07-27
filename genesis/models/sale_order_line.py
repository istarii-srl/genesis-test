from odoo import fields, api, models

class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    employee_ids = fields.Many2many('hr.employee', string="Employé(s)")