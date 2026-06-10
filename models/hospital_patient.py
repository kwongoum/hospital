from datetime import datetime
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit =["mail.thread", "mail.activity.mixin"]
    # _rec_name = "ref_patie"
    _rec_name = "name"


    name = fields.Char(string="Name",  tracking=True, required=True)
    
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute = "_compute_age", store= True)

    @api.depends("date_of_birth")
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                age = today.year - record.date_of_birth.year - ((today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day))
                record.age = age
            else:
                record.age = 0
                
    active = fields.Boolean(string="Active", default=True)
  
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female")], 
        string="Gender", tracking=True
    )
 
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address", default=" Rue ...")
    
    admission_date = fields.Datetime(string="Admission Date")
    discharge_date = fields.Datetime(string="Discharge Date")

    ref_patient = fields.Char(string="Reference Patient", compute="_compute_ref_patient", store=True)
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

    @api.depends("name")
    def _compute_ref_patient(self):
        for record in self:
            record.ref_patient = f"REF-PAT-{record.name[:3].upper()}-{record.id}"

    def action_admit(self):
        self.state = "admitted"

    def action_discharge(self):
        self.state = "discharged"
