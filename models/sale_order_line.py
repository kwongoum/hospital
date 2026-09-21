
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError



class SaleOrderLine(models.Model):
    
    _inherit = 'sale.order.line'
   
    discount_reason = fields.Selection([('insurance', 'Insurance'), ('low_income', 'Low Income'),
                                          ('chronic_condition', 'Chronic Condition'),
                                        ('other', 'Other')], string='Discount Reason')
    