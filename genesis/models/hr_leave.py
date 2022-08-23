from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import timedelta
import logging


_logger = logging.getLogger(__name__)

class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'
    _name = 'hr.leave'
    _description = 'hr.leave'

    def to_map(self):
        return {
            'id': self.id,
            'type': self.holiday_status_id.to_map()
        }

    @api.ondelete(at_uninstall=False)
    def _unlink_if_correct_states(self):
        error_message = _('You cannot delete a time off which is in %s state')
        state_description_values = {elem[0]: elem[1] for elem in self._fields['state']._description_selection(self.env)}
        now = fields.Datetime.now()

        if not self.env.is_superuser() and not self.user_has_groups('hr_holidays.group_hr_holidays_user'):
            if any(hol.state not in ['draft', 'confirm'] for hol in self):
                raise UserError(error_message % state_description_values.get(self[:1].state))
            if any(hol.date_from < now for hol in self):
                raise UserError(_('You cannot delete a time off which is in the past'))
        else:
            for holiday in self.filtered(lambda holiday: holiday.state not in ['draft', 'cancel', 'confirm']):
                raise UserError(error_message % (state_description_values.get(holiday.state),))