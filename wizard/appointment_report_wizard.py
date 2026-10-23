from odoo import api, models, fields
from odoo.exceptions import ValidationError
import logging
logger = logging.getLogger(__name__)


class AppointmentReportWizard(models.TransientModel):
   
    _name = "appointment.report.wizard"
    _description = "Appointment Report Wizard"
       
    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient")
    
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    
     
      
    def action_print_report(self):
        self.ensure_one()

        if not self.patient_id:
            raise ValidationError("Veuillez sélectionner un patient.")

        data = {
            "patient_id": self.patient_id.id,
            "date_from": self.date_from,
            "date_to": self.date_to,
        }

        return self.env.ref("hospital.action_report_patient_appointment_template"
        ).report_action(self.patient_id, data=data)

    @api.constrains("date_from", "date_to")
    def _check_date_range(self):
        for wizard in self:
            if (
                wizard.date_from
                and wizard.date_to
                and wizard.date_from > wizard.date_to
            ):
                raise ValidationError(
                    "start date must be less than or equal to end date. Please select a valid date range."
                )
                
    def action_print_xlsx_report(self):
        self.ensure_one()
        if not self.patient_id:
            raise ValidationError("Veuillez sélectionner un patient.")
        
        data={
            "patient_id": self.patient_id.id,
            "date_from": self.date_from,
            "date_to": self.date_to
        }
        return self.env.ref("hospital.action_report_appointment_xlsx").report_action(self, data=data)
    