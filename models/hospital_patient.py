from asyncio.log import logger
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging 
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit =["mail.thread", "mail.activity.mixin"]
    # _rec_name = "ref_patie"
    _rec_name = "name"
 
    # Fields definition
    name = fields.Char(string="Name",  tracking=True, required=True)
    
    date_of_birth = fields.Date(string="Date of Birth")
    is_birthday= fields.Boolean(string="Is Birthday", compute="_compute_is_birthday", store=True)
    age = fields.Integer(string="Age", compute = "_compute_age",
                         inverse="_inverse_age",
                         search="_search_age",
                         help="age is computed based on the date of birth")
    parent_phone = fields.Char(string="Parent Phone")
    marital_status = fields.Selection(
        selection=[("single", "Single"), ("married", "Married")],
        string="Marital Status"
    )
    spouse_name = fields.Char(string="Spouse Name")
    active = fields.Boolean(string="Active", default=True)

    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female")], 
        string="Gender", tracking=True, default="male"
    )
 
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    website = fields.Char(string="Website")
    code= fields.Text(string="Code")
    address = fields.Text(string="Address", default=" Rue ...")
    
    admission_date = fields.Datetime(string="Admission Date")
    discharge_date = fields.Datetime(string="Discharge Date")

    ref_patient = fields.Char(string="Ref. Patient", compute="_compute_ref_patient", store=True)
    ref_patient_sequence = fields.Char(string="Ref. Pat. Seq.", readonly=True, copy=False, default="New")
    
    notes = fields.Text(string="Notes")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("admitted", "Admitted"),
            ("discharged", "Discharged"),
        ],
        default="draft",
        string="Status",
    )
    image_1920= fields.Image(string="Image patient", max_width=1020, max_height=1920)
    is_covered =fields.Boolean(string="Is Covered by Insurance", default=False)
    tag_ids = fields.Many2many(comodel_name="hospital.patient.tag",string="Tags",  help="Select tags for the patient", 
                               ondelete='cascade'
                               )
    appointment_count = fields.Integer(string="Appoint.Cnt", compute="_compute_appointment_count", store=True)
    appointment_ids = fields.One2many(comodel_name="hospital.appointment", inverse_name="patient_id", string="Appointments")
    

     # override methods
            
    @api.model
    def create(self, vals):
        _logger.info(f"Creating a new patient with values: {vals}")
        if vals.get('ref_patient_sequence', 'New') == 'New':
            vals['ref_patient_sequence'] = self.env['ir.sequence'].next_by_code(
                'hospital.patient') or 'New'
            _logger.info(f"Assigned new sequence number: {vals['ref_patient_sequence']}")
        return super().create(vals)
        
    def write(self, vals):
            if vals.get('name'):
                vals['name'] = vals['name'].upper()
            return super().write(vals)   
    
    def name_get(self):
        result = []
        for patient in self:
              name = f"{patient.ref_patient_sequence} - {patient.name}"
              result.append((patient.id, name))
        return result

 

    # compute methods
    """   @api.depends("appointment_ids")
    def _compute_appointment_count(self):
        for record in self:
            record.appointment_count = len(record.appointment_ids)""" 
            
    @api.depends("appointment_ids")
    def _compute_appointment_count(self):
        grouped_data = self.env["hospital.appointment"].read_group(
            [("patient_id", "in", self.ids)],
            ["patient_id"],
            ["patient_id"])

        counts = {
            item["patient_id"][0]: item["patient_id_count"]
            for item in grouped_data
            }
        for patient in self:
            patient.appointment_count = counts.get(patient.id, 0)        
        
    @api.depends("date_of_birth")
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                
                if record.date_of_birth > today:
                      record.age = 0
                      continue
                   
                record.age = (
                  today.year
                  - record.date_of_birth.year
                  - (
                    (today.month, today.day)
                    < (record.date_of_birth.month, record.date_of_birth.day)
                   )
                )
            else:
                record.age = 0
    
        """ 
        def _inverse_age(self):
        for record in self:
            if record.age and record.age is not None:
                today = fields.Date.today()
                birth_year = today.year - record.age
                record.date_of_birth = date(birth_year, today.month, today.day) """        
          
    def _inverse_age(self):
        for record in self:
         if record.age:
            today = fields.Date.today()

            record.date_of_birth = (
                today - relativedelta(years=record.age)
            ) 
    @api.depends("name")
    def _compute_ref_patient(self):
        for record in self: 
            name_part = record.name[:3].upper() if record.name else "N/A"   
            record.ref_patient = f"REF-PAT-{name_part}-{record.id or'Neww'}"
    
    @api.depends("date_of_birth")
    def _compute_is_birthday(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                record.is_birthday = (
                    record.date_of_birth.month == today.month
                    and record.date_of_birth.day == today.day
                )
            else:
                record.is_birthday = False  
                

    # API Constraints 
    @api.constrains("date_of_birth")
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError("Incorrect: Date of birth cannot be in the future.")
            
    # _sql constraints
            
    # Onchange methods
    @api.onchange("age")
    def _onchange_age(self):
        if self.age:
            today = fields.Date.today()
            birth_year = today.year - self.age
            self.date_of_birth = date(
            birth_year,
            today.month,
            today.day
        )

    # Actions methods
    def action_admit(self):
        for record in self:
            if record.state != "draft":
                raise ValidationError("You can only admit a patient in draft state.")
            record.admission_date = fields.Datetime.now()
            record.state = "admitted"
       
    def action_discharge(self):
        self.state = "discharged"

     # others methods
     
    @api.ondelete(at_uninstall=False)
    def _check_patient_delete(self):
        _logger.info("========== ONDELETE PATIENT APPELE ==========")
        for record in self:
          if record.appointment_ids:
            _logger.info(
                f"Patient {record.name} has appointments and cannot be deleted."
            )
            raise UserError(
                f"Le patient {record.name} possède encore "
                "des rendez-vous et ne peut pas être supprimé."
            )
    def action_view(self):
            pass    
    
    def action_view_appointments(self):
        self.ensure_one()

        return {
        "type": "ir.actions.act_window",
        "name": "Appointments",
        "res_model": "hospital.appointment",
        "view_mode": "tree,form",
        "domain": [
            ("patient_id", "=", self.id)
        ],
        "context": {
            "default_patient_id": self.id
        },
        "target": "current"}
          
          
            # ========= search methods ===========
            
    def _search_age(self, operator, value):
        today = fields.Date.today()
        date_from = ( today - relativedelta(years=value + 1)+ relativedelta(days=1))
        date_to = today - relativedelta(years=value)
        
        if operator == "=":
            return [
            ("date_of_birth", ">=", date_from),
            ("date_of_birth", "<=", date_to),
            ]

        elif operator == ">":
             return [
              ("date_of_birth", "<", date_from),
             ]

        elif operator == ">=":
            return [
            ("date_of_birth", "<=", date_to),
            ]

        elif operator == "<":
            return [
            ("date_of_birth", ">", date_to),
            ]

        elif operator == "<=":
            return [
            ("date_of_birth", ">=", date_from),
            ]

        elif operator == "!=":
            return [
            "|",
            ("date_of_birth", "<", date_from),
            ("date_of_birth", ">", date_to),
            ]

        return []
    