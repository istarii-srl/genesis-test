from odoo import models

class ProjectProject(models.Model):

    _inherit = 'project.project'
    _name = 'project.project'

    def to_map(self):
        return {
            'id': self.id,
            'name': self.name,
            'client': self.partner_id.name if self.partner_id else "",
            'tasks': [task.to_map() for task in self.task_ids],
        }