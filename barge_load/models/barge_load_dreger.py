import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Dredger(models.Model):
    _name = 'barge.load.dredger'
    _description = 'Dredger Information'

    name = fields.Char(required=True)
    owner_id = fields.Many2one('res.partner', required=True)
    captain_id = fields.Many2one('captain', required=True)
