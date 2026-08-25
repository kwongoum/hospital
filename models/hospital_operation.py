from odoo import models, fields, api

class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False  # Disable automatic logging of create/write/unlink operations
    _rec_name = "operation_name"    
    _order = "sequence, id"
    doctor_id = fields.Many2one("hospital.doctor", string="Doctor")
    operation_name= fields.Char(string="Operation Name")
    reference_record= fields.Reference(string="Reference Record",
                                       selection=[("hospital.appointment", "Appointment"),
                                                  ("hospital.patient", "Patient")])
    sequence = fields.Integer(string="Reference", default=10)
    @api.model
    def name_create(self, name):
        record = self.create({"operation_name": name,})
        return record.name_get()[0]
 