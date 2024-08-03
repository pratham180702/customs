from odoo import api, fields, models
import odoo
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger('-------MY_MODEL-------')


class PartnerExistsWizard(models.TransientModel):
    _name = 'partner.exists.wizard'

    no_label = fields.Text(string="this phone already exist do you still want to continue?")

    @api.model
    def create_phone_contact(self):
        return {'type': 'ir.actions.act_window_close'}


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = "Hospital's Patient field"
    _rec_name = "ref"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _fold_name = 'fold'

    name = fields.Char(string='Name')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    ref = fields.Char(string="Reference Number")
    hospital = fields.Many2one("hospital.hospital", string="Admitted in")
    disease_ids = fields.One2many("hospital.diseases", "patient_id", string="Infected BY")
    cured = fields.Selection([('cured', 'Cured'), ('not_cured', 'Not Cured')], string="Health Status",
                             default='not_cured')
    patient_hobby = fields.Many2many("patient.hobby", "patient_hobby_rel", "ref", "hobby_id", string="Hobbies")
    patient_image = fields.Binary('Image')

    user_id = fields.Many2one('res.users', string='User', default=lambda x: x.env.user.id)
    status = fields.Selection(selection=[
        ('admitted', 'Patient Admitted'),
        ('treatment', 'Treatment In Progress'),
        ('cured', 'Patient Cured & Discharged'),
        ('not_cured', 'Dead'),
    ], string='Status', required=True, copy=False,
        tracking=True, default='admitted')
    admission = fields.Date(string='Admission Date')
    expected_date_of_release = fields.Date(string='Expected Release')
    date_of_release = fields.Date(string="Date of Release", readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    drugs = fields.One2many("drug.lines", "patient_id", string="Drugs")
    quantity = fields.Integer(string="Qty")
    total_bill = fields.Monetary(string="Total Bill", compute='_calculate_total_estimated_bill')
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    sequence = fields.Integer(string="sequence", default=10)

    fold = fields.Boolean(string='Folded in Kanban', default=True,
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    phone = fields.Integer(string="Phone")
    email = fields.Char(string="Email")

    # treated_under = fields.Many2one(
    #     'res.users',
    #     string='Treated Under',
    #     domain="[('id', 'in', filtered_doctor_ids)]",
    #     help='Doctor treating the patient',
    #     tracking=True
    # )

    _order = "sequence,name desc"

    # filtered_doctor_ids = fields.One2many(
    #     'res.users',
    #     compute='_compute_filtered_doctor_ids',
    #     string='Filtered Doctor IDs',
    #     store=False  # You may set store=True if you want this field to be stored in the database
    # )

    bmi = fields.Float(string="BMI", readonly=True)

    @api.depends('drugs')
    def _calculate_total_estimated_bill(self):
        total = 0
        for drug in self.drugs:
            total += (drug.drug_price * drug.quantity)
        self.total_bill = total

    @api.depends()
    def _compute_filtered_doctor_ids(self):
        doctors = self.env['res.users'].search([]).filtered(lambda a: a.has_group('pk_hospital.group_hospital_doctor'))
        self.filtered_doctor_ids = doctors.ids

    @api.onchange('cured')
    def change_status(self):
        try:
            self.status = 'admitted'
            if self.cured == 'cured':
                self.status = 'cured'
                _logger.info("STATUS CHANGED OF ALL THE PATIENTS FROM NOT CURED TO CURED")
        except Exception as e:
            _logger.exception("An error occurred: %s", e)

    def mark_as_cured(self):
        patients_to_mark_as_cured = self.search([('cured', '=', 'not_cured')])
        print(patients_to_mark_as_cured)
        patients_to_mark_as_cured.write({'cured': 'cured'})
        _logger.info("sample logger")
        return True

    def show_drugs(self):
        # Get the current patient's ID
        patient_id = self.id

        domain = [('patient_id', '=', patient_id)]

        # Return an action to open the drug lines associated with the current patient
        return {
            'name': 'Drug Lines',
            'res_model': 'drug.lines',
            'view_mode': 'tree',
            'view_id': self.env.ref('pk_hospital.show_drugs').id,
            'target': 'new',
            'type': 'ir.actions.act_window',
            'domain': domain,
        }

    def sample(self):
        _logger.info("STATUS CHANGED OF ALL THE PATIENTS FROM NOT CURED TO CURED")

        # conf = odoo.tools.config
        #
        # # Define domain expression using a list of tuples
        # domain = [('gender', '=', 'male')]
        #
        # # Use the domain expression to search for hospital patients
        # sample_model = self.env['hospital.patient'].search(domain)
        # print(sample_model)
        #
        # ex_id = [6, 1, 8]
        # print(self.env['hospital.patient'].browse(ex_id))
        #
        # # Print other information
        # print(conf['addons_path'])
        # path_list = conf['addons_path'].split(',')
        # print(odoo.release.version)
        # print(path_list)


    def action_share_whatsapp(self):
        if not self.phone:
            raise ValidationError("Missing Phone Number of the patient")
        mess = f'Hi, {self.name}'
        whatsapp_url = f'https://api.whatsapp.com/send?phone={self.phone}&text={mess}'

        self.message_post(body=mess, subject = 'Whatsapp Message')

        return {
            'type' : 'ir.actions.act_url',
            'target':'new',
            'url': whatsapp_url,
        }

    def button_in_progress(self):
        self.write({
            'status': "treatment"
        })

    def button_cured(self):
        self.write({
            'status': "cured"
        })

    def button_dead(self):
        self.write({
            'status': "not_cured"
        })

    @api.depends('name')
    def _compute_button_visibility(self):
        for record in self:
            record.button_visibility = record.name == ''

    button_visibility = fields.Boolean(compute='_compute_button_visibility', store=True)

    def date_of_release_confirm(self):
        self.date_of_release = self.expected_date_of_release

    def unlink(self):
        for patient in self:
            if patient.status == 'treatment':
                raise UserError("Cannot delete patient while in treatment state.")
        return super(HospitalPatient, self).unlink()

    # def read(self, fields=None, load='_classic_read'):
    #     # Check if 'status' field is requested and contains 'treatment'
    #     if fields and 'status' in fields and self.status == 'treatment':
    #         # Call super() with a domain filter to retrieve only 'treatment' patients
    #         return super(HospitalPatient, self.search([('status', '=', 'treatment')])).read(fields, load)
    #     else:
    #         # If 'status' is not requested or if the status is not 'treatment', proceed with default read()
    #         return super(HospitalPatient, self).read(fields, load)

    def copy(self, default=None):
        copied_patients = super(HospitalPatient, self).copy(default)

        for patient in copied_patients:
            patient.age += 1

        return copied_patients

    @api.model
    def create(self, vals):
        phone_number = vals.get('phone')

        partner_vals = {
            'name': vals.get('name'),
            'phone': vals.get('phone'),
        }
        partner = self.env['res.partner'].sudo().create(partner_vals)

        # Assign partner ID to the patient
        vals['partner_id'] = partner.id

        # Call the original create method
        return super(HospitalPatient, self).create(vals)

    def action_bill(self):
        pass


class DrugLines(models.Model):
    _name = "drug.lines"

    patient_id = fields.Many2one('hospital.patient', string="Patient", invisible=True)
    drug_id = fields.Many2one('hospital.drug', string="Drug")
    name = fields.Char(related='drug_id.name', string='Drug Name')
    drug_price = fields.Monetary(related='drug_id.drug_price', string='Price')
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id.id, readonly=True)

    quantity = fields.Integer(string="Qty")
    total = fields.Float(string="Total", compute='_compute_total')

    @api.depends('drug_price', 'quantity')
    def _compute_total(self):
        count = 0
        for record in self:
            print(f'entered for {count}')
            count += 1
            record.total = record.drug_price * record.quantity


# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     test_field = fields.Char(string="Sample Field")