# -*- coding: utf-8 -*-
{
    'name': "Intranet",

    'summary': """
        Intranet to publish company news and resources.
        """,

    'description': """
        Contains sections to publish company news, photos, documents and manuals.
    """,

    'application': True,

    'author': "Antonio Aguilar",
    'website': "http://www.onekeysystems.com.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/intranet_security.xml',
        'security/ir.model.access.csv',
        'views/intranet.xml',
        'views/post_views.xml',
        'views/intranet_menu.xml',
        'data/post_category.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}