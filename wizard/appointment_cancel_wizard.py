from odoo import api, models, fields
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)
class AppointmentCancelWizard(models.TransientModel):
   

    _name = "appointment.cancel.wizard"
    _description = "Appointment Cancel Wizard"
   
    def default_get(self, fields):
        res = super(AppointmentCancelWizard, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            appointment = self.env['hospital.appointment'].browse(active_id)
            res['appointment_id'] = appointment.id
        return res
     # fields definitions

    appointment_id = fields.Many2one(comodel_name="hospital.appointment", string="Appointment")
    reason = fields.Text( string="Reason(s)")
    
    def action_cancel(self):
        logger.info("Cancelling appointment. self value===========================%s", self)
        for record in self:
            appointment = record.appointment_id 
            logger.info(" Appointment value===========================%s", appointment)
            appointment_date = fields.Datetime.context_timestamp(self,appointment.appointment_date).date()
            if appointment and appointment_date == fields.Date.context_today(self):
                raise ValidationError("You cannot cancel an appointment scheduled for today.")
            appointment.write({'state': 'cancelled'})
        
        
              
            return {
            "type":"ir.actions.client",
            "tag": "reload"
        } 

