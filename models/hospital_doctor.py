from odoo import fields, models


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"

    name = fields.Char(string="Name", required=True)

    specialities = fields.Many2many("hospital.speciality", string="Specialities")
    email = fields.Char(string="Email")
