
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    line_number = fields.Integer(string='Line Number', index=True)
    
    @api.model
    def create(self, vals):
       _logger.warning("ACCOUNT MOVE LINE CREATE: %s", vals)

       record = super().create(vals)

       _logger.warning(
        "CREATED LINE %s - line_number=%s",
        record.id,
        record.line_number)

       return record