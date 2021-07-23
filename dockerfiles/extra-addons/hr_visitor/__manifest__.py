# -*- coding: utf-8 -*-

# Part of Spantree Ltd. See LICENSE file for full copyright and licensing details.
{
    'name': "Human Resource - Company Visitors Pass",
    'summary': """Company Visitors Pass & Details (Human Resource)""",
    'description': """
        HR Visitor Process module for company visit.
Tags:
company visitor
visitor process 
hr visitor process
visitor pass
visitor report
company visit
employee visitors
odoo visitor
visit company
pass print
    """,
    'author': "SpantreeNG",
    'website': 'www.spantreeng.com',
    'live_test_url': 'http://visitordemo.spantreeng.com',
    'category': 'Human Resources',
    'price': 15000.0,
    'currency': 'NGN',
    'version': '1.0',
    'depends': ['base','hr', 'mail','students'],
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'datas/visitor_sequence.xml',
            'views/visitor_process.xml',
            'reports/visitor_report.xml',
            'reports/visitor_badge.xml',
            'reports/visitor_student_report.xml',

            'views/mail_template.xml',

            ],
    'installable': True,
    'application': False,
}

