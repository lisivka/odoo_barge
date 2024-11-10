import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Quarry(models.Model):
    _name = 'barge.load.quarry'
    _description = 'Quarry Information'

    name = fields.Char()
    owner_id = fields.Many2one('res.partner')
    location = fields.Char()
    act_ids = fields.One2many('barge.load.act',
                              'quarry_id',
                              )
