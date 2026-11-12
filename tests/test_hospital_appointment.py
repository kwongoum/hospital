from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import ValidationError, UserError


class TestHospitalAppointment(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestHospitalAppointment, cls).setUpClass()

        cls.Patient = cls.env["hospital.patient"]
        cls.Appointment = cls.env["hospital.appointment"]

        cls.patient = cls.Patient.create(
            {
                "name": "John Doe",
                "phone": "+32 470-123-456",
            }
        )

    def _create_appointment(self, **values):
        """Helper method to create an appointment."""
        vals = {
            "patient_id": self.patient.id,
        }
        vals.update(values)

        return self.Appointment.create(vals)

    # --------------------------------------------------
    # 1. CREATE AND DEFAULT VALUES
    # --------------------------------------------------

    def test_create_appointment(self):
        appointment = self._create_appointment()

        self.assertTrue(appointment.id)
        self.assertEqual(appointment.patient_id, self.patient)
        self.assertEqual(appointment.state, "draft")
        self.assertTrue(appointment.active)
        self.assertTrue(appointment.appointment_date)
        self.assertEqual(appointment.description, " standard checkup")

    # --------------------------------------------------
    # 2. COMPUTED FIELDS
    # --------------------------------------------------

    def test_compute_ref_appointment(self):
        appointment = self._create_appointment()

        expected_ref = f"REF-APPOINT-JOH-{appointment.id}"

        self.assertEqual(appointment.ref_appointment, expected_ref)

    def test_compute_progress_draft(self):
        appointment = self._create_appointment()

        self.assertEqual(appointment.progress, 25)

    def test_compute_progress_in_consultation(self):
        appointment = self._create_appointment()

        appointment.state = "in_consultation"

        self.assertEqual(appointment.progress, 50)

    def test_compute_progress_done(self):
        appointment = self._create_appointment()

        appointment.state = "done"

        self.assertEqual(appointment.progress, 100)

    def test_compute_progress_cancelled(self):
        appointment = self._create_appointment()

        appointment.state = "cancelled"

        self.assertEqual(appointment.progress, 0)

    def test_patient_name_related_field(self):
        appointment = self._create_appointment()

        self.assertEqual(appointment.patient_name, self.patient.name)

    def test_gender_related_field(self):
        appointment = self._create_appointment()

        self.assertEqual(appointment.gender, self.patient.gender)

    # --------------------------------------------------
    # 3. NAME GET
    # --------------------------------------------------

    def test_name_get(self):
        appointment = self._create_appointment()

        expected_name = f"{appointment.ref_appointment} - {self.patient.name}"

        result = appointment.name_get()

        self.assertEqual(result[0][1], expected_name)

    # --------------------------------------------------
    # 4. WRITE VALIDATIONS
    # --------------------------------------------------

    def test_write_done_with_prescription(self):
        appointment = self._create_appointment()

        appointment.write(
            {
                "state": "done",
            }
        )

        self.assertEqual(appointment.state, "done")

    def test_write_done_without_prescription(self):
        appointment = self._create_appointment(prescription=False)

        with self.assertRaises(ValidationError):
            appointment.write(
                {
                    "state": "done",
                }
            )

    # --------------------------------------------------
    # 5. UNLINK VALIDATIONS
    # --------------------------------------------------

    def test_unlink_draft_appointment(self):
        appointment = self._create_appointment()

        appointment.unlink()

        self.assertFalse(appointment.exists())

    def test_unlink_non_draft_appointment(self):
        appointment = self._create_appointment(state="in_consultation")

        with self.assertRaises(ValidationError):
            appointment.unlink()

    # --------------------------------------------------
    # 6. ONCHANGE
    # --------------------------------------------------

    def test_onchange_patient_id(self):
        form = Form(self.Appointment)

        form.patient_id = self.patient

        self.assertEqual(form.description, f"Appointment for {self.patient.name}")

        self.assertEqual(form.state, "draft")

        self.assertEqual(form.ref_patient_sequence, self.patient.ref_patient_sequence)

    # --------------------------------------------------
    # 7. ACTION METHODS
    # --------------------------------------------------

    def test_action_in_consultation(self):
        appointment = self._create_appointment()

        result = appointment.action_in_consultation()

        self.assertEqual(appointment.state, "in_consultation")

        self.assertEqual(result["effect"]["type"], "rainbow_man")

    def test_action_reset_to_draft(self):
        appointment = self._create_appointment(state="in_consultation")

        appointment.action_reset_to_draft()

        self.assertEqual(appointment.state, "draft")

    def test_action_done(self):
        appointment = self._create_appointment(state="in_consultation")

        result = appointment.action_done()

        self.assertEqual(appointment.state, "done")

        self.assertEqual(result["tag"], "display_notification")

        self.assertEqual(result["params"]["type"], "success")

    def test_action_done_from_draft(self):
        appointment = self._create_appointment()

        with self.assertRaises(ValidationError):
            appointment.action_done()

    # --------------------------------------------------
    # 8. WINDOW ACTIONS
    # --------------------------------------------------

    def test_action_open_patient(self):
        appointment = self._create_appointment()

        action = appointment.action_open_patient()

        self.assertEqual(action["res_model"], "hospital.patient")

        self.assertEqual(action["res_id"], self.patient.id)

        self.assertEqual(action["target"], "new")

    def test_action_open_appointment(self):
        appointment = self._create_appointment()

        action = appointment.action_open_appointment()

        self.assertEqual(action["res_model"], "hospital.appointment")

        self.assertEqual(action["res_id"], appointment.id)

        self.assertEqual(action["target"], "new")

    def test_action_view_xray(self):
        appointment = self._create_appointment()

        action = appointment.action_view_xray()

        self.assertEqual(action["type"], "ir.actions.act_url")

        self.assertEqual(action["target"], "new")

    # --------------------------------------------------
    # 9. WHATSAPP
    # --------------------------------------------------

    def test_action_whatsapp(self):
        appointment = self._create_appointment()

        action = appointment.action_whatsapp()

        self.assertEqual(action["type"], "ir.actions.act_url")

        self.assertIn("wa.me/32470123456", action["url"])

        self.assertIn("text=", action["url"])

    def test_action_whatsapp_without_phone(self):
        patient = self.Patient.create(
            {
                "name": "Patient Without Phone",
            }
        )

        appointment = self._create_appointment(patient_id=patient.id)

        with self.assertRaises(UserError):
            appointment.action_whatsapp()
