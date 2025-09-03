from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError
# import logging

# logger = logging.getLogger(__name__)
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmer_id = fields.Many2one(
        'res.users', 
        string='Confirmed by', 
        tracking=True,
        help='Sales Manager who approved and confirmed this quotation',
        copy=False,
    )
    # MINIMAL OVERRIDE - Only adds tracking, keeps everything else same
    user_id = fields.Many2one(tracking=True)
    date_order = fields.Datetime(tracking=True)

    def action_confirm(self):
        """
        Overrides the original action to add a wizard
        before comfirming the sale order.
        """
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            raise AccessError(_("Only Sales Manager can confirm sales orders, please contact your manager."))
        
        if len(self) == 1 and not self.env.context.get('skip_confirm_wizard'):
            action = self.env['ir.actions.act_window']._for_xml_id('gopify_sale.action_sale_confirm_wizard')
            action['context'] = {
                'default_sale_order_id': self.id,
                'default_confirmation_message': _('Are you sure you want to confirm quotation %s?') % self.name,
                'default_quotation_date': self.date_order if self.date_order else False,
            }
            return action
        
        return super().action_confirm()
