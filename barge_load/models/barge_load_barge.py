import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class Barge(models.Model):
    _name = 'barge.load.barge'
    _description = 'Barge Information'

    name = fields.Char()
    owner_id = fields.Many2one('res.partner')
    cargo_capacity_per_cm = fields.Float(
        string="Average Cargo Capacity per cm",
        help="Average Cargo Capacity per cm "
             "(as per registration documents or calibration certificate)",
        digits=(7, 3),
    )
    act_ids = fields.One2many('barge.load.act',
                              'quarry_id',
                              )
