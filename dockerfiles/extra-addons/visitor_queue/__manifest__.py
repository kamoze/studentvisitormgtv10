# -*- coding: utf-8 -*-

{
    'name': "Queue Autorefresh",
    'summary': "visitor queue Autorefresh",
    'description': """
This module adds support for barcodes scanning to the visitor management system.
A barcode is generated for each visitor and printed on the badge.
    """,
    'author': 'Geo Technosoft',
    'website': 'www.geotechnosoft.com',
    'category': 'Tools',
    'depends': ['hr_visitor', 'web'],
    'data': [

        'queue_view.xml',
        'template_view.xml',


    ],

}
