# docker exec -it odoo-web odoo -u hospital -d hospital-db
from datetime import datetime
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"


    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    birthdate = fields.Date(string="Birthdate")
    active = fields.Boolean(string="Active", default=True)
    birthdate_fr = fields.Char(string="Birthdate FR", compute="_compute_birthdate_fr")

    @api.depends("birthdate")
    def _compute_birthdate_fr(self):
        for rec in self:
            if rec.birthdate:
                rec.birthdate_fr = rec.birthdate.strftime("%d/%m/%Y")
            else:
                rec.birthdate_fr = ""

    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female")], string="Gender"
    )

    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    image = fields.Binary(String="Image")
    is_urgent = fields.Boolean(string="Is Urgent Case")
    admission_date = fields.Datetime(string="Admission Date")
    discharge_date = fields.Datetime(string="Discharge Date")

    medical_history = fields.Text(string="Medical History")
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
