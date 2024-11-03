import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class BargeLoadingAct(models.Model):
    _name = 'barge.load.act'
    _description = 'Barge Loading Act'
    _inherit = ['mail.thread']

    number = fields.Char(tracking=True)
    date = fields.Date(tracking=True)

    quarry_id = fields.Many2one('barge.load.quarry', tracking=True)
    # owner_quarry_id = fields.Many2one(
    #     'res.partner',
    #     compute="_compute_owner_quarry_id",
    #     store=True,
    #     tracking=True
    # )
    owner_quarry_id = fields.Many2one('res.partner', string='Owner Quarry',
                                      compute='_compute_owner_quarry_id',
                                      store=True)

    receiver_id = fields.Many2one('res.partner', tracking=True)

    dredger_agent_id = fields.Many2one('res.partner', tracking=True)
    tugboat_agent_id = fields.Many2one('res.partner', tracking=True)

    dredger_id = fields.Many2one('barge.load.dredger', tracking=True)
    barge_id = fields.Many2one('barge.load.barge', tracking=True)
    tugboat_id = fields.Many2one('barge.load.tugboat', tracking=True)
    cargo_carrier_id = fields.Many2one(
        'res.partner',
        compute="_compute_cargo_carrier_id",
        store=True,
        tracking=True
    )

    status = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('done', 'Done'),
        ],
        default='draft',
        copy=False,
        tracking=True
    )

    # Work Time
    start_time = fields.Datetime(tracking=True)
    end_time = fields.Datetime(tracking=True)
    duration = fields.Float(
        compute="_compute_duration",
        string="Loading Duration (h)",
    )

    # ----- START ship`s draft
    before_left_nose = fields.Float(string="Before Left Nose (cm)")
    before_left_mid = fields.Float(string="Before Left Mid (cm)")
    before_left_stern = fields.Float(string="Before Left Stern (cm)")

    before_right_nose = fields.Float(string="Before Right Nose (cm)")
    before_right_mid = fields.Float(string="Before Right Mid (cm)")
    before_right_stern = fields.Float(string="Before Right Stern (cm)")

    after_left_nose = fields.Float(string="After Left Nose (cm)")
    after_left_mid = fields.Float(string="After Left Mid (cm)")
    after_left_stern = fields.Float(string="After Left Stern (cm)")

    after_right_nose = fields.Float(string="After Right Nose (cm)")
    after_right_mid = fields.Float(string="After Right Mid (cm)")
    after_right_stern = fields.Float(string="After Right Stern (cm)")

    before_avg_draft = fields.Float(
        compute="_compute_before_avg_draft",
        string="Before Avg Draft (cm)",
        digits=(6, 3)
    )
    after_avg_draft = fields.Float(
        compute="_compute_after_avg_draft",
        string="After Avg Draft (cm)",
         digits=(6, 3),
    )

    draft_difference = fields.Float(
        compute="_compute_draft_difference",
        string="Difference of Average Draft Before and After Loading (cm)",
        digits=(6, 3)
    )
    # ----- END ship`s draft

    # ----- START cargo capacity
    cargo_capacity_per_cm = fields.Float(
        related='barge_id.cargo_capacity_per_cm',
        string="Average Cargo Capacity per cm",
        help="Average Cargo Capacity per cm "
             "(as per registration documents or calibration certificate)",
        readonly=True,
        tracking=True
    )

    calculated_weight = fields.Float(
        compute="_compute_calculated_weight",
        string="Calculated Weight (t)",
        help="Calculated Weight of Water-Saturated Sand (t)",
        digits=(6, 3))
    moisture_coefficient = fields.Float(
        string="Moisture Coefficient (%)",
        help="Moisture Coefficient for Determining Recorded Weight (%)",
        default=22,
        digits=(3, 1),
    )
    record_weight = fields.Float(
        compute="_compute_record_weight",
        string="Record Weight (t)",
        help="Record Weight of Water-Saturated Sand (t)",
        digits=(6, 3),

    )

    @api.depends('quarry_id')
    def _compute_owner_quarry_id(self):
        for record in self:
            if record.quarry_id:
                record.owner_quarry_id = record.quarry_id.owner_id
            else:
                record.owner_quarry_id = None

    @api.depends('tugboat_id')
    def _compute_cargo_carrier_id(self):
        for record in self:
            if record.tugboat_id:
                record.cargo_carrier_id = record.tugboat_id.owner_id
            else:
                record.cargo_carrier_id = None

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            record.duration = 0
            if record.start_time and record.end_time:
                duration = record.end_time - record.start_time
                record.duration = duration.total_seconds() / 3600

    @api.depends('before_left_nose', 'before_left_mid', 'before_left_stern',
                 'before_right_nose', 'before_right_mid', 'before_right_stern')
    def _compute_before_avg_draft(self):
        for record in self:
            record.before_avg_draft = (record.before_left_nose +
                                       record.before_left_mid +
                                       record.before_left_stern +
                                       record.before_right_nose +
                                       record.before_right_mid +
                                       record.before_right_stern
                                       ) / 6

    @api.depends('after_left_nose', 'after_left_mid', 'after_left_stern',
                 'after_right_nose', 'after_right_mid', 'after_right_stern')
    def _compute_after_avg_draft(self):
        for record in self:
            record.after_avg_draft = (record.after_left_nose +
                                      record.after_left_mid +
                                      record.after_left_stern +
                                      record.after_right_nose +
                                      record.after_right_mid +
                                      record.after_right_stern
                                      ) / 6

    @api.depends('before_avg_draft', 'after_avg_draft')
    def _compute_draft_difference(self):
        for record in self:
            record.draft_difference = (record.after_avg_draft -
                                       record.before_avg_draft)

    #
    @api.depends('draft_difference', 'cargo_capacity_per_cm')
    def _compute_calculated_weight(self):
        for record in self:
            record.calculated_weight = (record.draft_difference *
                                        record.cargo_capacity_per_cm)

    #
    @api.depends('calculated_weight', 'moisture_coefficient')
    def _compute_record_weight(self):
        for record in self:
            record.record_weight = record.calculated_weight * (
                    1 - record.moisture_coefficient / 100)
