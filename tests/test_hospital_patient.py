from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError
from odoo import fields
from datetime import date
from dateutil.relativedelta import relativedelta


class TestHospitalPatient(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestHospitalPatient, cls).setUpClass()

        cls.Patient = cls.env["hospital.patient"]

        cls.patient = cls.Patient.create(
            {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "0470000000",
                "date_of_birth": date(1990, 5, 15),
            }
        )

    # ==========================================
    # 1. TEST CREATE
    # ==========================================

    def test_01_create_patient(self):
        """Test patient creation."""

        patient = self.Patient.create(
            {
                "name": "Alice Martin",
                "email": "alice@example.com",
            }
        )

        self.assertTrue(patient.id)
        self.assertEqual(patient.name, "Alice Martin")
        self.assertEqual(patient.state, "draft")
        self.assertTrue(patient.ref_patient_sequence)
        self.assertNotEqual(patient.ref_patient_sequence, "New")

    # ==========================================
    # 2. TEST WRITE
    # ==========================================

    def test_02_write_patient_name(self):
        """Test uppercase conversion when writing a name."""

        self.patient.write({"name": "peter parker"})

        self.assertEqual(self.patient.name, "PETER PARKER")

    # ==========================================
    # 3. TEST NAME_GET
    # ==========================================

    def test_03_name_get(self):
        """Test custom patient display name."""

        result = self.patient.name_get()

        expected_name = f"{self.patient.ref_patient_sequence} - " f"{self.patient.name}"

        self.assertEqual(result[0][0], self.patient.id)
        self.assertEqual(result[0][1], expected_name)

    # ==========================================
    # 4. TEST COMPUTE AGE
    # ==========================================

    def test_04_compute_age(self):
        """Test computed patient age."""

        today = fields.Date.today()

        birth_date = today - relativedelta(years=30)

        patient = self.Patient.create(
            {
                "name": "Age Test",
                "date_of_birth": birth_date,
            }
        )

        self.assertEqual(patient.age, 30)

    def test_05_compute_age_without_birth_date(self):
        """Age must be zero without date of birth."""

        patient = self.Patient.create(
            {
                "name": "No Birth Date",
            }
        )

        self.assertEqual(patient.age, 0)

    # ==========================================
    # 5. TEST INVERSE AGE
    # ==========================================

    def test_06_inverse_age(self):
        """Test inverse method of age."""

        self.patient.age = 40

        expected_birth_date = fields.Date.today() - relativedelta(years=40)

        self.assertEqual(self.patient.date_of_birth, expected_birth_date)

    # ==========================================
    # 6. TEST COMPUTE REFERENCE
    # ==========================================

    def test_07_compute_ref_patient(self):
        """Test computed patient reference."""

        self.assertTrue(self.patient.ref_patient.startswith("REF-PAT-JOH-"))

    # ==========================================
    # 7. TEST COMPUTE BIRTHDAY
    # ==========================================

    def test_08_compute_is_birthday(self):
        """Test birthday computation."""

        today = fields.Date.today()

        patient = self.Patient.create(
            {
                "name": "Birthday Test",
                "date_of_birth": today,
            }
        )

        self.assertTrue(patient.is_birthday)

    def test_09_compute_is_not_birthday(self):
        """Test when patient birthday is different."""

        today = fields.Date.today()

        another_date = today - relativedelta(days=10)

        patient = self.Patient.create(
            {
                "name": "Another Birthday",
                "date_of_birth": another_date,
            }
        )

        self.assertFalse(patient.is_birthday)

    # ==========================================
    # 8. TEST CONSTRAINT DATE OF BIRTH
    # ==========================================

    def test_10_future_birth_date(self):
        """Future date of birth must raise ValidationError."""

        future_date = fields.Date.today() + relativedelta(days=1)

        with self.assertRaises(ValidationError):

            self.Patient.create(
                {
                    "name": "Invalid Patient",
                    "date_of_birth": future_date,
                }
            )

    # ==========================================
    # 9. TEST ACTION ADMIT
    # ==========================================

    def test_11_action_admit(self):
        """Test patient admission."""

        self.patient.action_admit()

        self.assertEqual(self.patient.state, "admitted")
        self.assertTrue(self.patient.admission_date)

    def test_12_action_admit_invalid_state(self):
        """Admission is only allowed from draft state."""

        self.patient.action_admit()

        with self.assertRaises(ValidationError):
            self.patient.action_admit()

    # ==========================================
    # 10. TEST ACTION DISCHARGE
    # ==========================================

    def test_13_action_discharge(self):
        """Test patient discharge."""

        self.patient.action_discharge()

        self.assertEqual(self.patient.state, "discharged")

    # ==========================================
    # 11. TEST DELETE
    # ==========================================

    def test_14_delete_patient_without_appointments(self):
        """Patient without appointments can be deleted."""

        patient = self.Patient.create(
            {
                "name": "Patient To Delete",
            }
        )

        patient_id = patient.id

        patient.unlink()

        deleted_patient = self.Patient.browse(patient_id)

        self.assertFalse(deleted_patient.exists())

    # ==========================================
    # 12. TEST SEARCH AGE
    # ==========================================

    def test_15_search_patient_by_age(self):
        """Test searching patients using computed age."""

        today = fields.Date.today()

        birth_date = today - relativedelta(years=30)

        patient = self.Patient.create(
            {
                "name": "Search Age Test",
                "date_of_birth": birth_date,
            }
        )

        result = self.Patient.search(
            [
                ("id", "=", patient.id),
                ("age", "=", 30),
            ]
        )

        self.assertIn(patient, result)

    # ==========================================
    # 13. TEST ACTION VIEW APPOINTMENTS
    # ==========================================

    def test_16_action_view_appointments(self):
        """Test appointment window action."""

        action = self.patient.action_view_appointments()

        self.assertEqual(action["res_model"], "hospital.appointment")

        self.assertEqual(action["domain"], [("patient_id", "=", self.patient.id)])

        self.assertEqual(action["context"]["default_patient_id"], self.patient.id)

    # ==========================================
    # 14. TEST DEFAULT VALUES
    # ==========================================

    def test_17_patient_default_values(self):
        """Test default values of patient fields."""

        patient = self.Patient.create(
            {
                "name": "Default Test",
            }
        )

        self.assertTrue(patient.active)
        self.assertEqual(patient.gender, "male")
        self.assertFalse(patient.is_covered)
        self.assertEqual(patient.state, "draft")
        self.assertEqual(patient.address, " Rue ...")
