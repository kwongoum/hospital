from asyncio.log import logger
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit =["mail.thread", "mail.activity.mixin"]
    # _rec_name = "ref_patie"
    _rec_name = "name"
    _logger = logging.getLogger(__name__)
    # Fields definition
    name = fields.Char(string="Name",  tracking=True, required=True)
    
    date_of_birth = fields.Date(string="Date of Birth")
    

    age = fields.Integer(string="Age", compute = "_compute_age", store= True, 
                         help="age is computed based on the date of birth")
                
    active = fields.Boolean(string="Active", default=True)

    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female")], 
        string="Gender", tracking=True, default="male"
    )
 
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address", default=" Rue ...")
    
    admission_date = fields.Datetime(string="Admission Date")
    discharge_date = fields.Datetime(string="Discharge Date")

    ref_patient = fields.Char(string="Reference Patient", compute="_compute_ref_patient", store=True)
    ref_patient_sequence = fields.Char(string="Reference Patient Sequence", readonly=True, copy=False, default="New")
    
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
    image_1920= fields.Image("Image patient", max_width=1020, max_height=1920)
    is_covered =fields.Boolean(string="Is Covered by Insurance", default=False)
    tag_ids = fields.Many2many(comodel_name="hospital.patient.tag",string="Tags",  help="Select tags for the patient", 
                               ondelete='restrict'
                               )



     # override methods
       
    @api.model
    def create(self, vals):
        if vals.get('ref_patient_sequence', 'New') == 'New':
            vals['ref_patient_sequence'] = self.env['ir.sequence'].next_by_code(
                'hospital.patient'
            ) or 'New'

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
         
      # Compute methods
      
    # @api.model_create_multi  
    # def create(self, vals_list):
    #  records = super().create(vals_list)
    #  for r in records:
    #      if r.name:
    #         r.ref_patient = f"REF-PAT-{r.name[:3].upper()}-{r.id}"
    #      return records

    
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

    @api.depends("name")
    def _compute_ref_patient(self):
        for record in self: 
            name_part = record.name[:3].upper() if record.name else "N/A"   
            record.ref_patient = f"REF-PAT-{name_part}-{record.id or'Neww'}"

    # Constraints 
    @api.constrains("date_of_birth")
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError("Incorrect: Date of birth cannot be in the future.")
            
    # Onchange methods
    

    # Actions methods
    def action_admit(self):
        self.state = "admitted"

    def action_discharge(self):
        self.state = "discharged"

