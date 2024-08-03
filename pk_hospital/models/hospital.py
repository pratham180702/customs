from odoo import api, fields, models
from odoo.exceptions import UserError

class Hospitals(models.Model):
    _name = 'hospital.hospital'
    _description = "The below contains the list of hospitals"

    name = fields.Char(string='Name')
    hospital_id = fields.Integer(string="ID")
    address = fields.Text(string="address")
    patient = fields.Many2one("hospital.patient", string="Hospital Owner ID")
    first_phase = fields.Integer(string="Phase 1 Medicines")
    second_phase = fields.Integer(string="Phase 2 Medicines")
    total = fields.Integer(string="Total", compute="_compute_total", inverse="compute_inverse", search="_search_total")
    # total = fields.Integer(string="Total", compute="_compute_on_change")
    owner_name = fields.Text(string="Owner name", compute="_compute_patient_name")

    @api.depends('first_phase', 'second_phase')
    def _compute_total(self):
        for record in self:
            record.total = record.first_phase + record.second_phase

    def compute_inverse(self):
        for record in self:
            record.second_phase = record.total - record.first_phase

    @api.onchange('first_phase')
    def _compute_on_change(self):
        for record in self:
            record.total = record.first_phase * 3

    def _search_total(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
        return [('total', operator, value)]

    @api.onchange('patient.name')
    def _compute_patient_name(self):
        for record in self:
            record.owner_name = record.patient.name


    def write(self, vals):
        records = self.env['hospital.hospital'].search([])
        for record in records:
            if vals['hospital_id'] == record.hospital_id:
                raise UserError("ID already exist")


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, order=None):
        args = args or []
        domain = []
        print("entered here")
        if name:
            print("entered name")
            domain = ['|', ('name', operator, name), ('hospital_id', operator, name)]
        return self._search(domain, limit=limit, order=order)

    # @api.model
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.name
    #         result.append((record.hospital_id, name))
    #     print(result)
    #     return result


# class HospitaHospitalInherited(models.Model):
#     _inherit = "hospital.hospital"
    # @api.model
    # def name_get(self):
    #     print("entered here")
    #     result = []
    #     for record in self:
    #         name = f"{record.name} ({record.hospital_id})"
    #         result.append((record.id, name))
    #     return result
    # @api.model
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.name
    #         result.append((record.hospital_id, name))
    #     print(result)
    #     return result




class HospitalDoctors(models.Model):
    _name = 'hospital.doctors'
    _description = "The below contains the list of doctors"
    _inherit = 'hospital.hospital'

    hospital = fields.Many2one('hospital.hospital', string="Hospital")
    doctor_name = fields.Char(string="Doctor Name")
    doctor_age = fields.Integer(string="Age")


