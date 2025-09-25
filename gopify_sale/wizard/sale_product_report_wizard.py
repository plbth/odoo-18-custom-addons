from odoo import models, fields
from odoo.tools import date_utils
from datetime import date
import calendar

class SaleReportWizard(models.TransientModel):
    _name = 'sale.product.report.wizard'
    _description = 'Sale Report Wizard'
    
    def _get_year(self):
        """
        Helper function to generate a list of years from 2020 to the current year.
        This is used for the 'year' selection field.
        """
        current_year = fields.Date.today().year
        return [(str(y), str(y)) for y in range(current_year, 2019, -1)]
    
    analysis_type = fields.Selection(
        selection=[
            ('month', 'Monthly'),
            ('quarter', 'Quarterly'),
        ],
        string='Analysis due to:',
        default='month',
        required=True
    )
    year = fields.Selection(
        selection=_get_year,
        string='Year',
        default=lambda *a: str(fields.Date.today().year),
        required=True
    )
    month = fields.Selection(
        selection=[(str(i), calendar.month_name[i]) for i in range(1, 13)],
        string='Month',
        default=lambda *a: str(fields.Date.today().month)
    )
    quarter = fields.Selection(
        selection=[
            ('1', 'Q1'),
            ('2', 'Q2'),
            ('3', 'Q3'),
            ('4', 'Q4'),
        ],
        string='Quarter'
    )
    
    
    def action_view_report(self):
        self.ensure_one()
        year = int(self.year)
        
        if self.analysis_type == 'month':
            month = int(self.month)
            _, last_day_of_month = calendar.monthrange(year, month)
            start_date = date(year, month, 1)
            end_date = date(year, month, last_day_of_month)

        elif self.analysis_type == 'quarter':
            quarter_month_map = {
                '1': (1, 3),
                '2': (4, 6),
                '3': (7, 9),
                '4': (10, 12),
            }
            start_month, end_month = quarter_month_map[self.quarter]
            _, last_day_of_end_month = calendar.monthrange(year, end_month)
            start_date = date(year, start_month, 1)
            end_date = date(year, end_month, last_day_of_end_month)


        # Use Odoo's date_utils to get the exact start and end datetime
        # This correctly handles timezones and sets time to 00:00:00 and 23:59:59
        start_datetime = date_utils.start_of(start_date, 'day')
        end_datetime = date_utils.end_of(end_date, 'day')

        domain = [
            ('order_id.state', '=', 'sale'),
            ('order_id.date_order', '>=', start_datetime),
            ('order_id.date_order', '<=', end_datetime)
        ]
        return {
            'name': 'View Sale Report',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'list,pivot,graph',
            'domain': domain,
        }