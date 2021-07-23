# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (c) 2012-TODAY Acespritech Solutions Pvt Ltd
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields
from openerp.tools.translate import _


class SmsConfig(models.Model):
    _name = 'sms.config'

    url =fields.Char('URL', size=64, default='http://api.infobip.com/api/v3/sendsms/plain')
    login =fields.Char('Login', size=64)
    password =fields.Char('Password', size=64)
    active = fields.Boolean('Active', default=True)
    sms_body = fields.Text("SMS Body")



class SmsGroup(models.Model):
    _name = 'sms.group'
    name = fields.Char('Name', size=64)
    partner_ids = fields.Many2many('res.partner', 'rel_group_partner1', 'group_id', 'partner_id',
                                    string="Customers")
    type = fields.Selection([('sms', 'SMS'), ('email', 'Email')], string='Type', default='sms')



class message_template(models.Model):
    _name = 'message.template'
    name = fields.Char('Name', size=64)
    type = fields.Selection([('sms', 'SMS'), ('email', 'Email')], string='Type',default='sms')
    message = fields.Text('Message')
    email_message = fields.Text('Message')
    subject = fields.Char('Subject')

