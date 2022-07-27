from odoo import fields, models

class ProjectProjectStage(models.Model):
    _name = 'project.project.stage'
    _inherit = 'project.project.stage'

    is_inactivity = fields.Boolean("Étape d'inactvitié", help="Définit si les projets dans cette étapes sont inactifs/terminés.")