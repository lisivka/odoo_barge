import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Captain(models.Model):
    _name = 'barge.load.captain'
    _description = 'Captain Information'


    partner_id = fields.Many2one('res.partner', string="Captain", required=True)
    license_number = fields.Char(string="License Number")
