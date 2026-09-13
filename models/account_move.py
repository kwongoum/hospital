from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    confirmed_user_id = fields.Many2one(
        "res.users",
        string="SO Confirmed By"
    )