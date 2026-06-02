
from odoo import fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit =["mail.thread", "mail.activity.mixin"]

  
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")
    description = fields.Char(string="Description", tracking=True, required=True)
    active = fields.Boolean(string="Active", default=True)
    appointment_date = fields.Datetime(string="Appointment Date", default=fields.Datetime.now) 
    booking_date = fields.Date(string="Booking Date", default=fields.Date.today)