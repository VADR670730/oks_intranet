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
        'views/assets.xml',
        'views/settings_views.xml',
        'views/post_views.xml',
        'views/document_views.xml',
        'views/photos_views.xml',
        'views/intranet_menu.xml',
        'data/post_category.xml',
        'data/document_category.xml',
        'data/ir_rule.xml',
        'data/document_extension.xml',
    ],
    'qweb': [
        "static/src/xml/oks_intranet_img_prev.xml",
    ],
    # only loaded in demonstration mode
    'demo': [],
}