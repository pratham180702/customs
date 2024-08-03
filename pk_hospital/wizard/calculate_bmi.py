from odoo import api, models, fields


class CalculateBMI(models.TransientModel):
    _name = 'calculate.bmi'
    _description = 'Calculate the BMI of the Patient'

    def _default_patient_name(self):
        patient_id = self.env['hospital.patient'].browse(self.env.context.get('active_id'))
        return patient_id.name

    name = fields.Char(string="Patient's Name", default=_default_patient_name, readonly=True)
    height = fields.Float(string="Patient's Height in m", default=1)
    weight = fields.Float(string="Patient's Weight in kg")
    bmi = fields.Float(string="BMI", compute='calculate_bmi')

    @api.depends('height', 'weight')
    def calculate_bmi(self):
        self.bmi = (self.weight) / ((self.height)*(self.height))
        self.env['hospital.patient'].browse(self.env.context.get('active_id')).bmi = self.bmi
