from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
# import logging

# logger = logging.getLogger(__name__)
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # MINIMAL OVERRIDE - Only adds tracking, keeps everything else same
    user_id = fields.Many2one(tracking=True)
    date_order = fields.Datetime(tracking=True)

    def action_confirm(self):
        """
        Overrides the original action to add a wizard
        before comfirming the sale order.
        """
        if len(self) == 1 and not self.env.context.get('skip_confirm_wizard'):
            action = self.env['ir.actions.act_window']._for_xml_id('gopify_sale.action_sale_confirm_wizard')
            action['context'] = {
                'default_confirmation_message': _('Are you sure you want to confirm quotation %s?') % self.name,
                'default_sale_order_id': self.id,
                'default_quotation_date': self.date_order if self.date_order else False,
            }
            return action
        
        return super().action_confirm()
