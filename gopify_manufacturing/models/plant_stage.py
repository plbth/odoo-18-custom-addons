from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class PlantStage(models.Model):
    _name = 'plant.stage'
    _description = 'Manufacturing Tree Develop Stage'
    _order = 'sequence, id'

    code = fields.Char(string='Stage Code', required=True)
    name = fields.Char(string='Stage Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10, help='Determines the order of stages')
    active = fields.Boolean(string='Active', default=True, help='Only active stages will be considered in manufacturing processes.')

    mrp_production_ids = fields.One2many('mrp.production', 'stage_id', string='Manufacturing Orders')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The code must be unique.'),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_used(self): # Prevent deletion of stages with associated manufacturing orders
        for stage in self:
            if stage.mrp_production_ids:
                raise UserError(_('Cannot delete stage "%s" with associated manufacturing orders.', stage.name))
            
    
    def write(self, vals):
        """Prevent archive (uncheck active) of stages with stage associated manufacturing orders."""
        if 'active' in vals and not vals['active']: # If trying to uncheck active
            for stage in self:
                if stage.mrp_production_ids:
                    raise ValidationError("Cannot archive stage with associated manufacturing orders.")
        return super().write(vals)