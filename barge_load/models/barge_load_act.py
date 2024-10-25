import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class BargeLoadingAct(models.Model):
    _name = 'barge.load.act'
    _description = 'Barge Loading Act'
    _inherit = ['mail.thread']

    name = fields.Char(required=True,
                       tracking=True)
    date = fields.Date(required=True,
                       tracking=True)
    dredger_supervisor_id = fields.Many2one('res.partner',
                                            required=True)
    client_representative_id = fields.Many2one('res.partner',

                                               required=True)
    barge_id = fields.Many2one('barge', required=True)
    tugboat_name = fields.Char()
    barge_owner_id = fields.Many2one(related='barge_id.owner_id',
                                     readonly=True)
    receiver_id = fields.Many2one('res.partner',
                                  required=True)
    loading_start_time = fields.Datetime(required=True)
    loading_end_time = fields.Datetime(required=True)
    loading_duration = fields.Float(compute="_compute_loading_duration")

    # Осадки судна
    before_loading_nose = fields.Float(string="Before Loading Nose (cm)")
    before_loading_mid = fields.Float(string="Before Loading Mid (cm)")
    before_loading_stern = fields.Float(string="Before Loading Stern (cm)")
    after_loading_nose = fields.Float(string="After Loading Nose (cm)")
    after_loading_mid = fields.Float(string="After Loading Mid (cm)")
    after_loading_stern = fields.Float(string="After Loading Stern (cm)")

    average_before_loading = fields.Float(
        compute="_compute_average_before_loading")
    average_after_loading = fields.Float(
        compute="_compute_average_after_loading")
    draft_difference = fields.Float(compute="_compute_draft_difference")

    # Розрахунки
    loading_capacity_per_cm = fields.Float(required=True)
    wet_sand_weight = fields.Float(compute="_compute_sand_weight_wet")
    moisture_coefficient = fields.Float(default=22.0)
    dry_sand_weight = fields.Float(compute="_compute_sand_weight_dry")

    # Підписи
    # dredger_supervisor_signature = fields.Binary()
    # client_representative_signature = fields.Binary()
    # ship_captain_signature = fields.Binary()

    # Поля для зв'язку з іншими моделями
    dredger_id = fields.Many2one('dredger', required=True)
    quarry_id = fields.Many2one('quarry', required=True)

    @api.depends('loading_start_time', 'loading_end_time')
    def _compute_loading_duration(self):
        for record in self:
            if record.loading_start_time and record.loading_end_time:
                duration = record.loading_end_time - record.loading_start_time
                record.loading_duration = duration.total_seconds() / 3600

    @api.depends('before_loading_nose', 'before_loading_mid',
                 'before_loading_stern')
    def _compute_average_before_loading(self):
        for record in self:
            record.average_before_loading = (record.before_loading_nose +
                                             record.before_loading_mid +
                                             record.before_loading_stern) / 3

    @api.depends('after_loading_nose', 'after_loading_mid',
                 'after_loading_stern')
    def _compute_average_after_loading(self):
        for record in self:
            record.average_after_loading = (record.after_loading_nose +
                                            record.after_loading_mid +
                                            record.after_loading_stern) / 3

    @api.depends('average_before_loading', 'average_after_loading')
    def _compute_draft_difference(self):
        for record in self:
            record.draft_difference = (record.average_after_loading -
                                       record.average_before_loading)

    @api.depends('draft_difference', 'loading_capacity_per_cm')
    def _compute_sand_weight_wet(self):
        for record in self:
            record.sand_weight_wet = (record.draft_difference *
                                      record.loading_capacity_per_cm)

    @api.depends('sand_weight_wet', 'moisture_coefficient')
    def _compute_sand_weight_dry(self):
        for record in self:
            record.sand_weight_dry = record.sand_weight_wet * (
                    1 - record.moisture_coefficient / 100)
