{
    'name': "Genesis Consult",

    'summary': """
        Genesis Consult""",

    'description': """
        Genesis Consult
    """,

    'author': "istarii",
    'website': "https://istarii.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'ERP',
    'license': 'OPL-1',
    'version': '15.0.0.0',


    # any module necessary for this one to work correctly
    'depends': ['base', 'token_auth'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
    ],
    'qweb': [
    ],
}