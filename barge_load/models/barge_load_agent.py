import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Agent(models.Model):
    _name = 'barge.load.agent'
    # _inherit = 'res.partner'
    _description = 'Dredger Agent'

    # name = fields.Char()
    name = fields.Char(compute="_compute_name", store=True)
    partner_id = fields.Many2one('res.partner', required=True,
                                 ondelete="cascade")
    # Додаємо поле, яке пов'язує особу з користувачем
    user_id = fields.Many2one('res.users',
                              help="The user linked to this person.")

    #
    @api.depends('partner_id')
    def _compute_name(self):
        for record in self:
            record.name = record.partner_id.name \
                if record.partner_id else "Unnamed Agent"
