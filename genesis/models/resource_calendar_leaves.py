from odoo import models, fields, api, _
from odoo.tools import date_utils

class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"
    _name = "resource.calendar.leaves"
    _description = "Resource Time Off Detail"

    year = fields.Integer("Année", compute="_compute_year", store=True)

    @api.depends("date_from")
    def _compute_year(self):
        for leave in self:
            leave.year = leave.date_from.year
    
    def to_map(self):
        for leave in self:
            return {
                "id": leave.id,
                "name": leave.name,
                "date_from": date_utils.json_default(leave.date_from),
                "date_to": date_utils.json_default(leave.date_to),
            }