import logging
from odoo import models, api
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _search_display_name(self, operator, value):
        _logger.info(f"--- gopify_sale: _search_display_name executing for value: '{value}' ---")
        # Step 1: Get the default search domain (which searches on 'name').
        # This is equivalent to [('name', operator, value)] for res.partner.
        initial_domain = super()._search_display_name(operator, value)

        # Step 2: Create a new search domain for phone and mobile fields.
        # Reuse the original operator and value.
        phone_domain = ['|', ('phone', operator, value), ('mobile', operator, value)]

        final_domain = expression.OR([initial_domain, phone_domain])

        return final_domain