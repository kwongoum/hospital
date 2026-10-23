import base64
from io import BytesIO
from odoo import models



class PatientCardXlsx(models.AbstractModel):
    _name = 'report.hospital.report_patient_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):

        # Create ONE worksheet for all patients
        sheet = workbook.add_worksheet('Patient Cards')

        # Formats
        bold = workbook.add_format({
            'bold': True,
            'valign': 'vcenter',
        })

        title_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': 'yellow',
            'border': 1,
        })

        age_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
        })

        # Column widths
        sheet.set_column('D:D', 16.86)
        sheet.set_column('E:E', 16.86)

        # Starting row (0-based): Excel row 5
        start_row = 4

        for obj in patients:

            # Title: D:E merged
            sheet.merge_range(
                start_row, 3,
                start_row, 4,
                'ID Card',
                title_format,
            )
            sheet.set_row(start_row, 25)

            # Photo: next four rows
            photo_row = start_row + 1

            for row in range(photo_row, photo_row + 4):
                sheet.set_row(row, 30)

            if obj.image_1920:
                image_data = BytesIO(
                    base64.b64decode(obj.image_1920)
                )

                sheet.insert_image(
                    photo_row, 3,
                    'patient_photo.png',
                    {
                        'image_data': image_data,
                        'x_scale': 1.30,
                        'y_scale': 1,
                        'object_position': 1,
                        'x_offset': 2,
                        'y_offset': 2,
                    },
)

            # Two empty rows after the photo
            # Name, Age and Reference follow
            name_row = start_row + 7
            age_row = start_row + 8
            reference_row = start_row + 9

            sheet.write(name_row, 3, 'Name', bold)
            sheet.write(name_row, 4, obj.name or '')

            sheet.write(age_row, 3, 'Age', bold)
            sheet.write(age_row, 4, obj.age or 0, age_format)

            sheet.write(reference_row, 3,'Reference', bold)
            sheet.write( reference_row, 4, obj.ref_patient_sequence or '')

            # Two blank rows before the next patient
            start_row += 12
