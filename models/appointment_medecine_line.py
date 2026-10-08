from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AppointmentMedicineLine(models.Model):
    _name = 'appointment.medicine.line'
    _description = 'Appointment Medicine Line'


    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', ondelete='cascade')
    medicine_id = fields.Many2one('product.product', string='Medicine')
    sl_nb = fields.Integer(string='Serial Number', readonly=True)
    price_unit = fields.Float(string='Unit Price', related='medicine_id.list_price', digits='Product Price', readonly=True)
    quantity = fields.Integer(string='Quantity', default=1)
    currency_id = fields.Many2one('res.currency', string='Currency', 
                                  related='appointment_id.currency_id', readonly=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', 
                                      currency_field='currency_id')
    
    # CRUD methods
    @api.model
    def create(self, vals):
        appointment_id = vals.get('appointment_id')

        if appointment_id:
           last_line = self.search(
            [('appointment_id', '=', appointment_id)],
            order='sl_nb desc',
            limit=1)

        vals['sl_nb'] = last_line.sl_nb + 1 if last_line else 1

        return super().create(vals)
    
    def unlink(self):
        appointments = self.mapped('appointment_id')

        result = super().unlink()

        for appointment in appointments:
            lines = self.search(
            [('appointment_id', '=', appointment.id)],
            order='sl_nb, id')

        for number, line in enumerate(lines, start=1):
            line.sl_nb = number

        return result
    
    
    # constraints
    @api.depends('price_unit', 'quantity')
    def _compute_price_subtotal(self):
        for line in self:
            line.price_subtotal=line.price_unit*line.quantity
            