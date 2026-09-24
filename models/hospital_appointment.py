from odoo.tools import html2plaintext
from odoo.exceptions import ValidationError
import logging
from odoo import api, fields, models
from urllib.parse import quote
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

class HospitalAppointment(models.Model):

    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit =["mail.thread", "mail.activity.mixin"]
    _rec_name="ref_appointment"
    _order="appointment_date desc, patient_name asc"
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.ref_appointment} - {record.patient_id.name}"
            result.append((record.id, name))
        return result
    
     # fields definitions

    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient", ondelete="cascade")
    patient_name= fields.Char(related='patient_id.name', string='Patient Name', store=True)
    #doctor_id=fields.Many2one("hospital.doctor",string="Doctor")
    doctor_id=fields.Many2one("res.users",string="Doctor")
    description = fields.Char(string="Description", tracking=10, required=True, default=" standard checkup")
    active = fields.Boolean(string="Active", default=True)
    appointment_date = fields.Datetime(string="Appointment Date", tracking=20 , default= fields.Datetime.now) 
    
    booking_date = fields.Date(string="Booking Date",  default=fields.Date.context_today)
    
    gender = fields.Selection(related="patient_id.gender", string="Gender")
    
    ref_appointment = fields.Char(string="Ref. Appointment", compute="_compute_ref_appointment", store=True)
    # ref_patient_sequence = fields.Char(string="Reference Patient Sequence", related="patient_id.ref_patient_sequence",
    #                                    readonly=True)

    operation_id = fields.Many2one("hospital.operation", string="Operation")
    ref_patient_sequence = fields.Char(string="Ref. Patient Seq.")
    prescription = fields.Html(string=" Prescription", default="<h3>Prescription</h3><p>Enter prescription details here...</p>")
    priority= fields.Selection(
        selection=[ ("0", "None"),("1", "Low"), ("2", "Medium"), ("3", "High")],
        string="Priority"
    )
    state = fields.Selection(
        selection=[("draft","Draft"), ("in_consultation","In Consultation"), ("done","Done"),("cancelled","Cancelled")],
        string="Status", default="draft" )
    
    appointment_medicine_line_ids = fields.One2many('appointment.medicine.line','appointment_id', 
                                                    string ="Medicine Lines")
    price_total = fields.Monetary(string="Total", compute="_compute_price_total", currency_field='currency_id')
   
    
    company_id= fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id= fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True)
  
    progress = fields.Integer(string="Progress", default=0, compute="_compute_progress")
    
    hide_price = fields.Boolean(string="Hide Price")
  
  
     #override methods
    def write(self, vals):
        if vals.get('state') == 'done':
            for appointment in self:
                prescription_text= html2plaintext(appointment.prescription or "").strip()
                if not prescription_text:
               
                    raise ValidationError(
                    "You cannot mark the appointment as done without a prescription."
                )
        return super(HospitalAppointment, self).write(vals)
    
    def unlink(self): 
        for record in self:
            if record.state != "draft":
                raise ValidationError("You cannot delete an appointment that is not in draft state.")
        return super().unlink()

     # Compute methods           
    @api.depends("patient_id")
    def _compute_ref_appointment(self):
        for record in self:
            if record.patient_id:
                record.ref_appointment = f"REF-APPOINT-{record.patient_id.name[:3].upper()}-{record.id}"
            else:
                record.ref_appointment = False
    
    @api.depends("state")
    def _compute_progress(self):
        for record in self:
            if record.state == "draft":
                record.progress = 25
            elif record.state == "in_consultation":
                record.progress = 50
            elif record.state == "done":
                record.progress = 100
            else:
                record.progress = 0
    
    @api.depends('appointment_medicine_line_ids.price_subtotal')
    def _compute_price_total(self):
            for appointment in self:
                total = sum(line.price_subtotal for line in appointment.appointment_medicine_line_ids)
                appointment.price_total = total
        
                
    # Onchange methods
    @api.onchange("patient_id")
    def onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.description= f"Appointment for {record.patient_id.name}"
                record.state = "draft"
                record.ref_patient_sequence = record.patient_id.ref_patient_sequence
                # record.ref = f"REF-{record.patient_id.name[:3].upper()}-{record.id}"
            else:
                record.description = "standard checkup"
                record.ref_appointment = False
                record.ref_patient_sequence = False

    
    # Actions methods     
    def action_open_patient(self):
        self.ensure_one()
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'hospital.patient',
        'res_id': self.patient_id.id,
        'view_mode': 'form',
        'target': 'new',  # ouvre en popup
        'context': {'form_view_initial_mode': 'view', 'readonly': True}
    }
        
    def  action_reset_to_draft(self):
        _logger.info("Resetting. self value===========================%s", self)
        for rec in self:
            rec.state = 'draft'    
    
    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': ' Successfully in consultation',
                    'type': 'rainbow_man'
                    }
            }
            
   
    """ 
    def action_done(self):
        appointments = self.filtered(lambda rec: rec.state == "in_consultation")

        if not appointments:
            raise ValidationError("You can only mark an appointment as Done if it is in consultation state.")
        appointments.write({ "state": "done" })
        action = self.env.ref("hospital.view_hospital_patient_form")
        return {
        "type": "ir.actions.client",
        "tag": "display_notification",
        "params": {
            "title": "Success 🎉",
            "message": f"{len(appointments)} consultation(s) completed successfully!",
            "type": "success",
            "sticky": False,
            "next": {"type": "ir.actions.act_window_close"},
            },
        }   """
        
        
    def action_done(self):
        appointments = self.filtered( lambda rec: rec.state == "in_consultation")
        if not appointments:
         raise ValidationError("You can only mark an appointment as Done if it is in consultation state.")

        appointments.write({"state": "done"})

        patient =  appointments[0].patient_id
        return {
    "type": "ir.actions.client",
    "tag": "display_notification",
    "params": {
        "title": "Success 🎉",
        "message": f"{len(appointments)} consultation(s) completed successfully!",
        "type": "success",
        "sticky": True,
        "next": {
            "type": "ir.actions.act_window",
            "name": "Patient",
            "res_model": "hospital.patient",
            "view_mode": "form",
            "res_id": patient.id,
            "views": [
                (
                    self.env.ref(
                        "hospital.view_hospital_patient_form"
                    ).id,
                    "form",
                )
            ],
            "target": "current",
        },
    },
}
       
        
        
        
    # def action_cancel(self):
    #     for rec in self:
    #         print("Cancelling appointment..........................................")
    #         rec.state = 'cancelled'

    def action_cancel_in_appointment(self):
        _logger.info("self = %s", self)
        _logger.info("self.env = %s", self.env)
        _logger.info( "action = %s",self.env.ref("hospital.action_appointment_cancel_wizard"))
        action= self.env.ref('hospital.action_appointment_cancel_wizard').read()[0]
        return action 

        
        
    def action_open_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',  # ouvre en popup
            'context': {'form_view_initial_mode': 'view', 'readonly': True}
        }
    def action_view_xray(self):
        
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "name": "X-Ray",
            "url": f"https://www.uzbrussel.be/fr/web/radiologie/vos-images-scann%C3%A9es",
            "target": "new"
        }
        
     
    def action_whatsapp(self):
        self.ensure_one()

        patient = self.patient_id

        if not patient.phone:
            raise UserError(
                "Patient does not have a phone number."
            )

        phone = patient.phone.replace("+", "")
        phone = phone.replace(" ", "")
        phone = phone.replace("-", "")

        message = (
            f"Hello *{patient.name}*,\n\n"
            f"We are contacting you regarding your *appointment* "
            f"on {self.appointment_date}.\n\n"
            f"_Thank you._"
        )

        url = (
            f"https://wa.me/{phone}"
            f"?text={quote(message)}"
        )
        self.message_post(subject="WhatsApp Message",
                          body=f"WhatsApp message sent to {patient.name} ({patient.phone})")
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }    
       
       
        # other methods
    def create_doctor_user(self):
        self.ensure_one()
        group_doctor = self.env.ref('base.group_user')  # exemple groupe

        user = self.env['res.users'].create({
            'name': 'Dr House2',
            'login': 'house2@hospital.com',
             'password': 'Doctor123',
            'groups_id': [(6, 0, [group_doctor.id])],
        })
        return user