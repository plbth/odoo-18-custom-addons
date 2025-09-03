from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.osv import expression
import logging

logger = logging.getLogger(__name__)

class SaleConfirmWizard(models.TransientModel):
    _name = 'sale.confirm.wizard'
    _description = 'Sale Order Confirmation Wizard with details'

    confirmation_message = fields.Char(string='Confirmation', readonly=True)
    quotation_date = fields.Datetime(string='Quotation Date', readonly=True, required=True)
    confirmation_date = fields.Datetime(string='Confirmation Date', default=fields.Datetime.now, required=True,
                                        help='This is the confirmation date on the sales order')

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', readonly=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', related='sale_order_id.team_id', readonly=True)
    confirmer_id = fields.Many2one('res.users', string='Confirm by', default=lambda self: self.env.user, help='Sales Manager approving this quotation')


    def action_confirm_order(self):
        self.ensure_one()

        valid_member = self.team_id.member_ids.filtered(lambda u: u.id == self.confirmer_id.id)
        if not valid_member:
            raise UserError(_("The selected user '%s' is not a member of the '%s' team. Please select a valid user.") % (
                self.confirmer_id.name, self.team_id.name
            ))

        # today = fields.Datetime.now()
        # if self.confirmation_date.date() < today.date():
        #     raise UserError(_('Confirmation date cannot be before today.'))
        """ If the above validation is used, we don't need the below validation.
            However, depends on your business logic, you might want to keep it.
            You can use either of the two approaches based on your requirements.
        """
        if self.confirmation_date < self.quotation_date:
            raise UserError(_('Confirmation date cannot be earlier than quotation date.'))

        order = self.sale_order_id
        order.write({
            'date_order': self.confirmation_date,
            'confirmer_id': self.confirmer_id.id,
        })
        # Confirm the order (bypass wizard)
        order.with_context(skip_confirm_wizard=True).action_confirm()

        return {'type': 'ir.actions.act_window_close'}