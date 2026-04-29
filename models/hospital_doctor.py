from odoo import models
from odoo import fields


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"

    name = fields.Char(string="Name", required=True)
