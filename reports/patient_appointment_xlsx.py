
from odoo import models


class PatientAppointmentXlsx(models.AbstractModel):
    _name = "report.hospital.report_patient_appointment_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Patient Appointment XLSX Report"

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet("Appointment Report")

        # Formats
        header_format = workbook.add_format({
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        # En-têtes
        sheet.write(0, 0, "NAME", header_format)
        sheet.write(0, 1, "REFERENCE", header_format)

        sheet.set_column("A:A", 25)
        sheet.set_column("B:B", 25)

        # Récupération des données du wizard
        data = data or {}
        patient_id = data.get("patient_id")
        date_from = data.get("date_from")
        date_to = data.get("date_to")

        if not patient_id:
            return

        patient = self.env["hospital.patient"].browse(
            int(patient_id)
        ).exists()

        if not patient:
            return

        # Domaine de recherche des rendez-vous
        domain = [
            ("patient_id", "=", patient.id),
        ]

        # Ajouter les critères de dates uniquement
        # lorsque les dates sont renseignées
        if date_from:
            domain.append(("appointment_date", ">=", date_from))

        if date_to:
            domain.append(("appointment_date", "<=", date_to))

        appointments = self.env["hospital.appointment"].search(
            domain,
            order="appointment_date, id",
        )

        # Une ligne Excel par rendez-vous
        row = 1

        for appointment in appointments:
            sheet.write(row, 0, patient.name or "")
            sheet.write(
                row,
                1,
                appointment.ref_appointment or "",
            )
            row += 1
