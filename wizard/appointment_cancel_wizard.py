from odoo import api, models, fields

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
        for record in self:
            appointment = record.appointment_id
            appointment.write({'state': 'cancelled'})

