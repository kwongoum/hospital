
from odoo import models
import logging

_logger = logging.getLogger(__name__)


class PatientAppointmentReport(models.AbstractModel):
    _name = "report.hospital.patient_appointment_template"
    
    _description = "Patient Appointment Report"

    def _get_report_values(self, docids, data=None):
        data = data or {}

        patient_id = (
            docids[0]
            if docids
            else data.get("patient_id")
        )

        docs = self.env["hospital.patient"].browse(
            patient_id
        ).exists()

        date_from = data.get("date_from")
        date_to = data.get("date_to")

        domain = [
            ("patient_id", "in", docs.ids),
        ]

        if date_from:
            domain.append(("appointment_date", ">=", date_from))

        if date_to:
            domain.append(("appointment_date", "<=", date_to))

        appointments = self.env["hospital.appointment"].search(domain)

        _logger.info("DOCIDS = %s", docids)
        _logger.info("PATIENT ID = %s", patient_id)
        _logger.info("PATIENTS = %s", docs.mapped("name"))

        return {
            "doc_ids": docs.ids,
            "doc_model": "hospital.patient",
            "docs": docs,
            "appointments": appointments,
            "date_from": date_from,
            "date_to": date_to,
        }
