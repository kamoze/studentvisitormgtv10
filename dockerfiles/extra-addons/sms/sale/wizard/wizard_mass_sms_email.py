# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-TODAY Acespritech Solutions Pvt Ltd
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
from odoo import models, api, fields
from odoo import tools, SUPERUSER_ID
import time
import urllib
import urllib2


class WizardMassSmsEmail(models.TransientModel):
    _name = 'wizard.mass.sms.email'

    msg_type = fields.Selection([('sms', 'SMS'), ('email', 'Email')], string='Message Type', default='sms')
    subject = fields.Char('Subject')
    message = fields.Text('Message')
    email_message = fields.Text('Message')
    send_option = fields.Selection([('group', 'Group'),
                                    ('all', 'All Customer'),
                                     ('selected', 'Selected')], string='Send Option', default='group')
    template_id = fields.Many2one('message.template', 'Template')
    group_id = fields.Many2one('sms.group', 'Group')
    customer_ids = fields.Many2many('res.partner', 'rel_partner_sms_email1',
                                    'wizard_id', 'partner_id', string='Customers')



    @api.onchange('msg_type', 'template_id')
    def onchange_template(self):
        result = {'value': {'message': False, 'subject': False}}
        if not self.template_id:
            return result
        template = self.template_id
        if self.msg_type == 'sms':
            result['value']['email_message'] = False
            result['value']['message'] = template.message or False
        else:
            result['value']['message'] = False
            result['value']['email_message'] = template.email_message or False
        result['value']['subject'] = template.subject or False
        return result


    @api.multi
    def action_send(self):
        sms_obj = self.env['sms.config']
        partner_obj = self.env['res.partner']
        mail_pool = self.env['mail.mail']
        user_pool = self.env['res.users']
        record = self
        #send SMS
        if record.msg_type == 'sms':
            mobiles = []
            if record.send_option == 'group' and record.group_id:
                for customer in record.group_id.partner_ids:
                    if customer.mobile:
                        mobiles.append(customer.mobile)
            elif record.send_option == 'all':
                 partner_ids = partner_obj.search([('customer','=',True)])
                 if partner_ids:
                    for part in partner_ids:
                        if part.mobile:
                            mobiles.append(part.mobile)
            else:
                for cust in record.customer_ids:
                    if cust.mobile:
                        mobiles.append(cust.mobile)
            sms_ids = sms_obj.search([('active', '=', True)])
            if sms_ids and mobiles:
                sms_rec = sms_obj.browse(sms_ids[0])
                url = str(sms_rec.url).strip()
                login = str(sms_rec.login).strip()
                password = str(sms_rec.password).strip()
                for mobile in mobiles:
                    params = urllib.urlencode({
                        'user': login,
                        'password': password,
                        'sender': 'OpenERP',
                        'GSM': mobile,
                        'SMSText': record.message,
                    })
                    try:
                        request = urllib2.Request(url, params)
                        response = urllib2.urlopen(request)
                        result = response.read()
                    except Exception, e:
                        pass
        #send Email
        else:
            recipient_ids = []
            if record.send_option == 'group' and record.group_id:
                for customer in record.group_id.partner_ids:
                    if customer.email:
                        recipient_ids.append(customer.id)
            elif record.send_option == 'all':
                 partner_ids = partner_obj.search([('customer','=',True)])
                 if partner_ids:
                    for part in partner_ids:
                        if part.email:
                            recipient_ids.append(part.id)
            else:
                for cust in record.customer_ids:
                    if cust.email:
                        recipient_ids.append(cust.id)
            if recipient_ids:
                user = self.env.user
                if user.company_id and user.company_id.email:
                    mail_id = mail_pool.create({
                        'email_from': user.company_id.email,
                        'subject': record.subject,
                        'body_html': record.email_message,
                        'auto_delete': True,
                        'recipient_ids': [(4, id) for id in recipient_ids]
                    })
                    mail_pool.send([mail_id])
        return {'type': 'ir.actions.act_window_close'}
