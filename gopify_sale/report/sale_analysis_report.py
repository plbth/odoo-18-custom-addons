from odoo import models, fields, api, tools
from odoo.tools import SQL

class TopProductReport(models.Model):
    _name = 'sale.order.report.analysis'
    _description = 'Top Product Report'
    _auto = False
    _order = 'total_sold DESC, product_id'

    product_id = fields.Many2one('product.product', readonly=True)
    #product_name = fields.Char('Product Name', readonly=True); # This is a translation field, data type: jsonb in db
    total_sold = fields.Float('Total Sold', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

    @api.model
    def _select(self):
        return """
            row_number() over() as id,
            sol.product_id,
            SUM(sol.product_uom_qty) AS total_sold,
            so.company_id
        """

    @api.model
    def _from(self):
        return """
            sale_order_line sol
            LEFT JOIN sale_order so ON sol.order_id = so.id
        """
    
    @api.model
    def _where(self):
        return """
            so.state IN ('sale', 'done')
        """
        
    @api.model
    def _group_by(self):
        return """
            sol.product_id,
            so.company_id
        """

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table) # or self._cr
        query = SQL("""
            CREATE OR REPLACE VIEW %(table)s AS
                SELECT    %(select)s
                FROM      %(from)s
                WHERE     %(where)s
                GROUP BY  %(group_by)s
                ORDER BY  total_sold DESC
                LIMIT     10
            """ % {
                'table': self._table,
                'select': self._select(),
                'from': self._from(),
                'where': self._where(),
                'group_by': self._group_by()
            }
        )
        self.env.cr.execute(query)