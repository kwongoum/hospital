from odoo import models,fields,api

class HospitalPatientTag(models.Model):
    _name = "hospital.patient.tag"
    _description = "Hospital Patient Tag"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(string="Active", default=True)