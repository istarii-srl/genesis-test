# -*- coding: utf-8 -*-
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Contacts"

    def to_map(self):
       for partner in self:
            return {
                "id": partner.id,
                "name": partner.name,
                "email": partner.email if partner.email else "",
            }