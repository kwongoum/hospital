from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AppointmentMedicineLine(models.Model):
    _name = 'appointment.medicine.line'
    _description = 'Appointment Medicine Line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    medicine_id = fields.Many2one('product.product', string='Medicine')
    price_unit = fields.Float(string='Unit Price', related='medicine_id.list_price', readonly=True)
    quantity = fields.Integer(string='Quantity', default=1)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_price_subtotal', store=True)
    
    @api.depends('price_unit', 'quantity')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal=line.price_unit*line.quantity
            