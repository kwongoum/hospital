
from odoo import models, fields, api

class SaleReport(models.Model):
    _inherit = "sale.report"

    confirmed_user_id = fields.Many2one("res.users", string="Confirmed By", readonly=True)

    #  add confirmed_user_id to the group by clause
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        groupby += ', s.confirmed_user_id'
        fields['confirmed_user_id'] = ", s.confirmed_user_id as confirmed_user_id"
        return super(SaleReport, self)._query(with_clause=with_clause, fields=fields, groupby=groupby, from_clause=from_clause)     
    
    