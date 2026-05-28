from odoo import models, fields

class HospitalSpeciality(models.Model):
    _name = "hospital.speciality"
    _description = "Hospital Speciality"

    name = fields.Char(string="Name", required=True)