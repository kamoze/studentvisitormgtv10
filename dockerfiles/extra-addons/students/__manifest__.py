# -*- coding: utf-8 -*-
{
    'name': "Students",

    'summary': """
        Containing the information about the Students""",

    'description': """
        Part of the Student Visitor management system from Spantree. 
    """,

    'author': "SpantreeNG",
    'website': "http://www.spantreeng.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail', 'project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/badge_report.xml',
        'views/visitor_student.xml',
        'views/visitor_school.xml',
        'views/visitor_parent.xml',
        'views/visitor_contarct.xml',
        'views/visitor_configuration.xml',
        'views/visitor_location.xml',
    ],
    # only loaded in demonstration mode
    
}
