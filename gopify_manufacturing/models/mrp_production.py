from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    plant_stage_id = fields.Many2one('plant.stage', string='Manufacturing Stage', ondelete='restrict', tracking=True)