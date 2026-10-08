from odoo import models,fields,api


class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'mail.thread', 'mail.activity.mixin']

    color =fields.Integer(tracking=True)