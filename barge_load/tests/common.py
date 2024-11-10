# tests/common.py
from odoo.tests.common import TransactionCase


class BargeLoadTestCommon(TransactionCase):
    """Common setup for Barge Load Act tests."""

    def setUp(self):
        super(BargeLoadTestCommon, self).setUp()
        self.BargeLoadingAct = self.env['barge.load.act']
