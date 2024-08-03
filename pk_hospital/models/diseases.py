from odoo import api, fields, models

class Diseases(models.Model):
    _name = 'hospital.diseases'
    _description = "The below contains the list of diseases"

    name = fields.Char(string='Name')
    description = fields.Text(string="Description")
    patient_id = fields.Many2one("hospital.patient", string="Patient")
