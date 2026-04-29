# docker exec -it odoo-web odoo -u hospital -d hospital-db

from odoo import fields
from odoo import models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    birthdate = fields.Date(format="%d-%m-%Y", string="Birthdate")
    gender = fields.Selection(
        fields.Selection(
            [fields.Selection("male", "Male"), fields.Selection("female", "Female")]
        )
    )
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    image = fields.Binary(String="Image")
    is_urgent = fields.Boolean(string="Is Urgent Case")
    admission_date = fields.Datetime(string="Admission Date")
    discharge_date = fields.Datetime(string="Discharge Date")
#   """   doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
#     department_id = fields.Many2one("hospital.department", string="Department") """
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