from odoo import models


class Task(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    def to_map(self):
        return {
            'id': self.id,
            'name': self.name,
        }