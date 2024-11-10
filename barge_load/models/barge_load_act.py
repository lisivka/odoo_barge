import logging

from datetime import datetime, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class BargeLoadingAct(models.Model):
    _name = 'barge.load.act'
    _description = 'Barge Loading Act'
    _inherit = ['mail.thread']

    number = fields.Char(tracking=True)
    date = fields.Date(tracking=True)

    quarry_id = fields.Many2one('barge.load.quarry', tracking=True)
    owner_quarry_id = fields.Many2one('res.partner', tracking=True)

    receiver_id = fields.Many2one('res.partner', copy=False,
                                  tracking=True)

    dredger_agent_id = fields.Many2one('barge.load.agent', copy=False,
                                       tracking=True)
    tugboat_agent_id = fields.Many2one('barge.load.agent', copy=False,
                                       tracking=True)

    dredger_id = fields.Many2one('barge.load.dredger', tracking=True)
    barge_id = fields.Many2one('barge.load.barge', copy=False,
                               tracking=True)
    tugboat_id = fields.Many2one('barge.load.tugboat', copy=False,
                                 tracking=True)
    cargo_carrier_id = fields.Many2one('res.partner', copy=False,
                                       tracking=True)

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
    start_time = fields.Datetime(copy=False, tracking=True)
    end_time = fields.Datetime(copy=False, tracking=True)
    duration = fields.Float(
        compute="_compute_duration",
        string="Duration (h)",
    )

    # ----- START ship`s draft
    before_left_nose = fields.Float(string="Before Left Nose (cm)",
                                    copy=False, tracking=True, )
    before_left_mid = fields.Float(string="Before Left Mid (cm)",
                                   copy=False, tracking=True, )
    before_left_stern = fields.Float(string="Before Left Stern (cm)",
                                     copy=False, tracking=True, )

    before_right_nose = fields.Float(string="Before Right Nose (cm)",
                                     copy=False, tracking=True, )
    before_right_mid = fields.Float(string="Before Right Mid (cm)",
                                    copy=False, tracking=True, )
    before_right_stern = fields.Float(string="Before Right Stern (cm)",
                                      copy=False, tracking=True, )

    after_left_nose = fields.Float(string="After Left Nose (cm)",
                                   copy=False, tracking=True, )
    after_left_mid = fields.Float(string="After Left Mid (cm)",
                                  copy=False, tracking=True, )
    after_left_stern = fields.Float(string="After Left Stern (cm)",
                                    copy=False, tracking=True, )

    after_right_nose = fields.Float(string="After Right Nose (cm)",
                                    copy=False, tracking=True, )
    after_right_mid = fields.Float(string="After Right Mid (cm)",
                                   copy=False, tracking=True, )
    after_right_stern = fields.Float(string="After Right Stern (cm)",
                                     copy=False, tracking=True, )

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
        digits=(6, 3),
        store=True
    )
    # ----- END ship`s draft

    # ----- START calculated weight
    cargo_capacity_per_cm = fields.Float(
        related='barge_id.cargo_capacity_per_cm',
        string="Capacity (t/cm)",
        help="Average Cargo Capacity ton per cm "
             "(as per registration documents or calibration certificate)",
        readonly=True,
        store=True,
        tracking=True,
    )
    calculated_weight = fields.Float(
        compute="_compute_calculated_weight",
        string="Calculated Weight (t)",
        help="Calculated Weight of Water-Saturated Sand (t)",
        digits=(6, 3),
        store=True,
        tracking=True,

    )
    moisture_coefficient = fields.Float(
        string="Moisture Coefficient (%)",
        help="Moisture Coefficient for Determining Recorded Weight (%)",
        default=22,
        store=True,
        digits=(3, 1),

    )
    record_weight = fields.Float(
        compute="_compute_record_weight",
        string="Record Weight (t)",
        help="Record Weight without Water (t)",
        digits=(6, 3),
        store=True,
        tracking=True
    )

    # ----- END calculated weight

    @api.onchange('quarry_id')
    def _onchange_quarry_id(self):
        if self.quarry_id:
            self.owner_quarry_id = self.quarry_id.owner_id

    @api.onchange('tugboat_id')
    def _onchange_cargo_carrier_id(self):
        if self.tugboat_id:
            self.cargo_carrier_id = self.tugboat_id.owner_id

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
            if record.draft_difference and record.cargo_capacity_per_cm:
                record.calculated_weight = (record.draft_difference *
                                            record.cargo_capacity_per_cm)

    @api.depends('calculated_weight', 'moisture_coefficient')
    def _compute_record_weight(self):
        for record in self:
            record.record_weight = (record.calculated_weight *
                                    (1 - record.moisture_coefficient / 100))

    @api.model
    def write(self, vals):

        """
        Override standard write method to prevent modification of fields other
        than 'status' or 'id' when the act status is set to 'Done'.

        """

        for record in self:
            if record.status == 'done':
                restricted_fields = [field for field in vals.keys() if
                                     field not in ['id', 'status']]

                if restricted_fields:
                    raise ValidationError(
                        _("You cannot modify  act - the status is 'Done'.")
                    )

        # Call base write method if checks passed
        return super(BargeLoadingAct, self).write(vals)

    last_7_days_date = fields.Date(compute='_compute_dates', store=False)
    last_30_days_date = fields.Date(compute='_compute_dates', store=False)

    @api.depends('date')
    def _compute_dates(self):
        for record in self:
            record.last_7_days_date = (datetime.now() -
                                       timedelta(days=7)).date()
            record.last_30_days_date = (datetime.now() -
                                        timedelta(days=30)).date()

    @api.model
    def default_get(self, field_names):
        res = super(BargeLoadingAct, self).default_get(field_names)
        return res

    def print_barge_load_act_report(self):

        return self.env.ref(
            'barge_load.action_report_barge_load_act').report_action(self)
