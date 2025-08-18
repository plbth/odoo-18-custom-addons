from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class PlantStage(models.Model):
    _name = 'plant.stage'
    _description = 'Manufacturing Tree Develop Stage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    code = fields.Char(string='Stage Code', required=True, tracking=True)
    name = fields.Char(string='Stage Name', required=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=1, help='Determines the order of stages')
    active = fields.Boolean(string='Active', default=True, help='Only active stages will be considered in manufacturing processes.', tracking=True)

    # Relations
    company_id = fields.Many2one('res.company', string='Company', default=lambda self:self.env.company, tracking=True)
    mrp_production_ids = fields.One2many('mrp.production', 'plant_stage_id', string='Manufacturing Orders', tracking=True)

    # Computed fields
    count_mrp = fields.Integer(compute="_compute_count_mrp_production", string="Manufacturing Count")

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'The code must be unique.'),
    ]

    @api.constrains('code')
    def _check_code_length(self):
        for record in self:
            if record.code and len(record.code) > 10:
                raise ValidationError("The code's length cannot exceed 10 characters.")

            
    @api.depends('mrp_production_ids')
    def _compute_count_mrp_production(self):
        for record in self:
            record.count_mrp = len(record.mrp_production_ids)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_used(self): # Prevent deletion of stages with associated manufacturing orders
        conflicting_stages = [
            record.code for record in self
            if record.mrp_production_ids
        ]
        if not conflicting_stages:
            return

        raise UserError(f"Cannot delete stages: {', '.join(conflicting_stages)} that is associated with manufacturing orders.")
    

    #  Work when the write() or create() method called, but must pay attention to its attribute, like mrp_production_ids, else 
    #  will be hard to debug in the future
    @api.constrains('active', 'mrp_production_ids')
    def _check_active(self):
        conflicting_stages = [
            record.code for record in self 
            if record.mrp_production_ids and not record.active
        ]
        
        if not conflicting_stages:
            return
            
        error_message = (
            f"Cannot archive stage: {conflicting_stages[0]}" 
            if len(conflicting_stages) == 1
            else f"Cannot archive these stages: {', '.join(conflicting_stages)}"
        )
        raise UserError(f"{error_message} (being used in production).")

    """ --- ALTERNATIVE METHODS CONSIDERED ---
    The following methods were tested as alternatives to the @api.constrains decorator
    for preventing the archiving of stages in use.
    """

    """ Alternative 1: Using @api.onchange
    This method only provides a client-side warning and does not prevent the user
    from saving the record, making it unsuitable for enforcing a strict rule.
    """
    # @api.onchange('active')
    # def _onchange_active(self):
    #     if self.active == False:  # If trying to archive
    #         if self.mrp_production_ids:
    #             self.active = True  # Revert the change
    #             return {
    #                 'warning': {
    #                     'title': 'Warning',
    #                     'message': f"Cannot archive stage '{self.code}' as it is being used in manufacturing."
    #                 }
    #             }

    """ Alternative 2: Overriding the write() method
    This is a powerful but more invasive approach. It's generally better to use
    @api.constrains for validation logic to keep business rules separate from
    core ORM methods. This should be considered a last resort.
    """
    # def write(self, vals):
    #     if 'active' in vals and not vals['active']: # If choose "Not active" while the stage is being used in manufacturing.
    #         conflicting_stages = [
    #             record.code for record in self
    #             if record.mrp_production_ids
    #         ]
    #         if not conflicting_stages:
    #             return super().write(vals)
            
    #         error_message = (
    #             f"Cannot archived stage: {conflicting_stages[0]}"
    #             if len(conflicting_stages) == 1
    #             else f"Cannot archive these stages: {', '.join(conflicting_stages)}"
    #         ) 
    #         raise UserError(f"{error_message} (being used in production).")
    #     return super().write(vals)

    def action_view_mrp_productions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Manufacturing Orders',
            'res_model': 'mrp.production',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.mrp_production_ids.ids)],
            'context': {'default_plant_stage_id': self.id} # In returned context, default_field help pre-fill when create new.
        }
