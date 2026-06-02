from datetime import datetime
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit =["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name",  tracking=True, required=True)
    age = fields.Integer(string="Age")
    birthdate = fields.Date(string="Birthdate")
    active = fields.Boolean(string="Active", default=True)
  
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female")], 
        string="Gender", tracking=True
    )
 
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    
    is_urgent = fields.Boolean(string="Is Urgent Case")
    admission_date = fields.Datetime(string="Admission Date")
    discharge_date = fields.Datetime(string="Discharge Date")

    ref = fields.Text(string="Reference")
    notes = fields.Text(string="Notes")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("admitted", "Admitted"),
            ("discharged", "Discharged"),
        ],
        default="draft",
        string="Status",
    )

    def action_admit(self):
        self.state = "admitted"

    def action_discharge(self):
        self.state = "discharged"
