from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    stage_id = fields.Many2one('plant.stage', string='Manufacturing Stage', domain="[('active', '=', True)]", )