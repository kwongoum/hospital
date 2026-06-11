
from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit =["mail.thread", "mail.activity.mixin"]

  
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")
    description = fields.Char(string="Description", tracking=True, required=True, default=" standard checkup")
    active = fields.Boolean(string="Active", default=True)
    appointment_date = fields.Datetime(string="Appointment Date", default= fields.Datetime.now) 
    
    booking_date = fields.Date(string="Booking Date",  default=lambda self: fields.Date.context_today(self))
    gender = fields.Selection(related="patient_id.gender", string="Gender")
    
    ref_appointment = fields.Char(string="Reference Appointment", compute="_compute_ref_appointment", store=True)
    prescription = fields.Html(string="Prescription")
    priority= fields.Selection(
        selection=[ ("0", "None"),("1", "Low"), ("2", "Medium"), ("3", "High")],
        string="Priority"
    )
    state = fields.Selection(
        selection=[("draft","Draft"), ("in_consultation","In Consultation"), ("done","Done"),("cancelled","Cancelled")],
        string="Status", default="draft" )
    
    def action_open_patient(self):
        self.ensure_one()
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'hospital.patient',
        'res_id': self.patient_id.id,
        'view_mode': 'form',
        'target': 'new',  # ouvre en popup
        'context': {'form_view_initial_mode': 'view', 'readonly': True}
    }
        
    def  action_reset_to_draft(self):
        for rec in self:
            rec.state = 'draft'    
    
    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'
            
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    
    def action_cancel(self):
        for rec in self:
            print("Cancelling appointment..........................................")
            rec.state = 'cancelled'
    @api.depends("patient_id")
    def _compute_ref_appointment(self):
        for record in self:
            if record.patient_id:
                record.ref_appointment = f"REF-APPOINT-{record.patient_id.name[:3].upper()}-{record.id}"
            else:
                record.ref_appointment = False
    
    @api.onchange("patient_id")
    def onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.description= f"Appointment for {record.patient_id.name}"
                record.state = "draft"
                # record.ref = f"REF-{record.patient_id.name[:3].upper()}-{record.id}"
            else:
                record.description = "standard checkup"
                record.ref_appointment = False
                