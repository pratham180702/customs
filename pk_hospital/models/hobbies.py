from odoo import api, fields, models
from odoo.exceptions import UserError


class Hobbies(models.Model):
    _name = 'patient.hobby'

    name = fields.Char(string='Name', default="sample name")
    hobby_id = fields.Integer(string="id")

    patients = fields.Many2many('hospital.patient', 'patient_hobby_rel', 'hobby_id', 'ref', string='Patients')

    _sql_constraints = [
        ('name_id_uniq', 'unique (name)', 'The hobby name must be unique!'),
        ('id_not_null', 'check (name IS NOT NULL)', 'The hobby name should not be null')
    ]

    # @api.model
    # def create(self, vals):
    #     if 'hobby_id' in vals:
    #         existing_record = self.env['patient.hobby'].search([('hobby_id', '=', vals['hobby_id'])])
    #         if existing_record:
    #             last_unique_id = self.env['patient.hobby'].search([], order='hobby_id desc', limit=1)
    #             raise UserError(f'Hobby ID must be unique! Last unique ID was : {last_unique_id[0]}')

        # return super(Hobbies, self).create(vals)

    # @api.constrains('name')
    # def _check_name(self):
    #     records = self.env['patient.hobby'].search([])
    #     for record in records:
    #         if self.name == record.name:
    #             raise UserError("The end date cannot be set in the past")


    def default_get(self, fields):
        res = super(Hobbies, self).default_get(fields)

        print("override.......................")
        res['name'] = 'Abc'
        print(res)
        return res
