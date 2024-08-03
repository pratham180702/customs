from odoo import api, fields, models
from odoo.exceptions import UserError


class Drugs(models.Model):
    _name = 'hospital.drug'

    name = fields.Char(string='Name')
    drug_id = fields.Integer(string="id")
    drug_price = fields.Monetary(string='Price')
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id.id)


    # @api.model
    # def create(self, vals):
    #     if 'drug_id' in vals:
    #         existing_record = self.env['hospital.drug'].search([('drug', '=', vals['drug_id'])])
    #         if existing_record:
    #             last_unique_id = self.env['hospital.drug'].search([], order='drug_id desc', limit=1)
    #             raise UserError(f'Drug ID must be unique! Last unique ID was : {last_unique_id[0]}')
    #
    #     return super(Drugs, self).create(vals)
