import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Dredger(models.Model):
    _name = 'barge.load.dredger'
    _description = 'Dredger Information'

    name = fields.Char()
    owner_id = fields.Many2one('res.partner')
    act_ids = fields.One2many('barge.load.act',
                              'quarry_id',
                              )
