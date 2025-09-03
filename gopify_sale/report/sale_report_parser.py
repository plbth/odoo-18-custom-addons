from odoo import models, api
from num2words import num2words
import logging

_logger = logging.getLogger(__name__)

class CustomQuotationReport(models.AbstractModel):
    _name = 'report.gopify_sale.template_custom_quotation'
    _description = 'Custom Quotation Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        This method is the core of the report engine.

        :param docids: A list of IDs of the records to print (e.g., [10, 15, 20] for sale.order).
        :param data: Optional data passed from wizards. Usually None for direct printing.
        :return: A dictionary of data to be passed to the QWeb template.
        """
        docs = self.env['sale.order'].browse(docids)

        def amount_to_text_vi(amount, currency):
            """Convert amount to Vietnamese text"""
            try:
                text_amount = num2words(amount, lang='vi').capitalize()

                if currency.upper() == 'VND':
                    return f"{text_amount} đồng"
                elif currency.upper() == 'USD':
                    return f"{text_amount} đô la Mỹ"
                else:
                    return f"{text_amount} {currency}"
            except Exception as e:
                _logger.error(f"Error converting amount to text: {e}")
                return f"{amount:,.0f} {currency}"

        def format_discount(discount):
            """Format discount percentage"""
            if discount > 0:
                return f"{discount:,.1f}%"
            return "-"

        def format_tax_rate(tax_ids):
            """Format tax rates"""
            if tax_ids:
                rates = [f"{tax.amount:,.0f}%" for tax in tax_ids]
                return ", ".join(rates)
            return "-"

        return {
            'doc_ids': docids, # Not needed in this module
            'docs': docs,
            'amount_to_text_vi': amount_to_text_vi,
            'format_discount': format_discount,
            'format_tax_rate': format_tax_rate,
        }