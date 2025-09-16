{
    'name': 'Gopify - Sale Customizations',
    'version': '1.0',
    'summary': 'Adds customer phone search and custom filters to Sales.',
    'category': 'Sales',
    'depends': ['sale','sale_management',],
    'data': [
        'security/ir.model.access.csv',
        'data/paperformat_data.xml',
        'views/sale_order_view.xml',
        'wizard/sale_confirm_wizard_view.xml',
        'views/sale_report_actions.xml',
        'views/sale_report_templates.xml',
        'report/sale_analysis_report_views.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'gopify_sale/static/src/scss/gopify_sale_report.scss',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}