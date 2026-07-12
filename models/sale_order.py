import logging
from odoo import models, fields, api

logging.basicConfig(level=logging.INFO)
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

        # fields definitions
    confirmed_user_id = fields.Many2one('res.users', string='Confirmed By')
    appointment_id = fields.Many2one('hospital.appointment',
                                     string='Appointment',
                                     ondelete='set null')         
    
    patient_id = fields.Many2one('hospital.patient',
                                     string='Patient',
                                     ondelete='set null')
    
        # actions  functions 
    def action_confirm(self):
         self.confirmed_user_id = self.env.user.id
         _logger.info("Commande confirmée ============== : %s", self.confirmed_user_id.name)
         return super(SaleOrder, self).action_confirm()
        