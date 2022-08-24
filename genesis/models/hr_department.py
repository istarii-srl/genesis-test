from email.policy import default
from odoo import fields, models, _


class Department(models.Model):
    _name = "hr.department"
    _description = "Department"
    _inherit = "hr.department"

    has_access_to_extranet = fields.Boolean("A accès à l'extranet", default=False)
    use_previsionnal = fields.Boolean("Timesheet prévisionnelle")
