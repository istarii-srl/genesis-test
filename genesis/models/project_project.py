from odoo import models

class ProjectProject(models.Model):

    _inherit = 'project.project'
    _name = 'project.project'

    def to_map(self):
        for project in self:
            return {
                'id': project.id,
                'name': project.name,
                'client': project.partner_id.name if project.partner_id else ""
            }