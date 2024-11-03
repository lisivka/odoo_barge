import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Tugboat(models.Model):
    _name = 'barge.load.tugboat'
    _description = 'Tugboat Information'

    name = fields.Char()
    owner_id = fields.Many2one('res.partner')


