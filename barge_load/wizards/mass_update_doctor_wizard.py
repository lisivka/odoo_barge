import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class MassUpdateActWizard(models.TransientModel):
    _name = 'mass.update.act.wizard'
    _description = 'Wizard for Mass Update of Acts'

    # Поле для вибору нового статусу
    new_status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done'),
        ],
        string="New Status",
        required=True
    )

    def action_update_act(self):
        # Отримуємо активні записи (акти), що були обрані
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            # Отримуємо обрані акти для оновлення
            acts = self.env['barge.load.act'].browse(active_ids)
            # Оновлюємо статус для кожного акта
            for act in acts:
                act.status = self.new_status
        return {'type': 'ir.actions.act_window_close'}
