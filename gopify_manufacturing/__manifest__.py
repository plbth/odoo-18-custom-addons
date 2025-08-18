{
    'name': 'Gopify Manufacturing',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Gopify Plant Stage Manufacturing Module',
    'depends': ['mrp'],
    'data': [
        'security/ir.model.access.csv',
        'security/plant_stage_security.xml',
        'views/plant_stage_view.xml',
        'views/plant_stage_menus.xml'
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}