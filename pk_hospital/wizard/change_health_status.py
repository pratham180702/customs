from odoo import api, models, fields

class ChangeHealthStatus(models.TransientModel):
    _name = 'change.health.status'
    _description = 'Change the Health status of the patient'

    ref = fields.Many2one('hospital.patient', string="Reference ID", display_name="ref")

    def update_health_status(self):
        for wizard in self:
            # Ensure a reference ID is selected
            if wizard.ref:
                # Update the health status of the referenced patient
                wizard.ref.cured = 'cured'
