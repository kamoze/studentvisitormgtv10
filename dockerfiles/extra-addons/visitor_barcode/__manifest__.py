# -*- coding: utf-8 -*-

{
    'name': "Visitor Barcode  Scanning",
    'summary': "Add barcode scanning feature to visitor.",
    'description': """
This module adds support for barcodes scanning to the visitor management system.
A barcode is generated for each visitor and printed on the badge.
    """,
    'author': 'Geo Technosoft',
    'website': 'www.geotechnosoft.com',
    'category': 'Tools',
    'depends': ['barcodes', 'hr_visitor', 'students'],
    'data': [

        'views/visitor_barcode.xml',
        'views/admission_barcode_template.xml',

    ],
    'qweb': [
        "static/src/xml/visitor_barcode.xml",
    ],
}
