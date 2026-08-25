from odoo import models,fields,api

class HospitalPatientTag(models.Model):
    _name = "hospital.patient.tag"
    _description = "Hospital Patient Tag"


    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color Index")
    active = fields.Boolean(string="Active", default=True, copy=False)
    sequence= fields.Integer(string="Sequence")
    #  sql constraints
    
    _sql_constraints=[ ('name_unique', 'unique(name)', 'Tag name must be unique. This on already exist !'),

                      ('sequence_positive', 'CHECK(sequence>0)', 'Sequence must not be a negative number!')]
    
    # override methods
    def copy(self, default=None):
        default = dict(default or {})
        copy_number = self.with_context(active_test=False).search_count([
        ('name', 'like', self.name + '%')])
        default['name'] = f"{self.name} ({copy_number})"
        return super().copy(default)