import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Barge(models.Model):
    _name = 'barge.load.barge'
    _description = 'Barge Information'

    name = fields.Char(required=True)
    owner_id = fields.Many2one('res.partner', required=True)
    captain_id = fields.Many2one('barge.load.captain', required=True)

