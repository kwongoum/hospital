from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AppointmentMedicineLine(models.Model):
    _name = 'appointment.medicine.line'
    _description = 'Appointment Medicine Line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    medicine_id = fields.Many2one('product.product', string='Medicine')
    price_unit = fields.Float(string='Unit Price', related='medicine_id.list_price', readonly=True)
    quantity = fields.Integer(string='Quantity', default=1)
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                  related='appointment_id.currency_id', readonly=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', 
                                      currency_field='currency_id')
    
    @api.depends('price_unit', 'quantity')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal=line.price_unit*line.quantity
            