import logging
from datetime import datetime, timedelta
from odoo import fields
from odoo.exceptions import ValidationError
from .common import BargeLoadTestCommon

_logger = logging.getLogger(__name__)


class TestBargeLoadingDuration(BargeLoadTestCommon):

    def test_01_compute_duration(self):
        """Test that duration is computed correctly based
        on start_time and end_time."""
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=5)  # 5 hours later

        # Create a record with specific start_time and end_time
        act = self.BargeLoadingAct.create({
            'number': 'Test001',
            'date': fields.Date.today(),
            'start_time': start_time,
            'end_time': end_time,
        })

        # Check that the computed duration is 5 hours
        self.assertEqual(act.duration, 5.0, "Duration should be 5 hours")

    def test_02_write_protection_on_done_status(self):
        """Test that fields other than 'status'
        cannot be modified when status is 'Done'."""

        # Create a record with status 'draft'
        act = self.BargeLoadingAct.create({
            'number': 'Test002',
            'date': fields.Date.today(),
            'status': 'draft',
        })

        # Change status to 'done'
        act.write({'status': 'done'})

        # Attempt to modify another field and expect a ValidationError
        with self.assertRaises(ValidationError):
            act.write({'number': 'NewNumber'})  # Should raise an error
