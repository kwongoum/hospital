from odoo import fields, models, api


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one("res.users", string="Odoo User", required=True)
    specialities = fields.Many2many("hospital.speciality", string="Specialities")
    email = fields.Char(string="Email")
    
   
