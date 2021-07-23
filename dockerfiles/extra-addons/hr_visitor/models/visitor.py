# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
import base64
import random
import urllib
import urllib2

class HrVisitorProcess(models.Model):
    _name = 'hr.visitor'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = 'in_datetime desc, id desc'

    @api.multi
    def get_barcode(self):
        width = 300
        height = 50
        humanreadable = 1
        barcode = self.env['report'].barcode(
            'Code128', self.barcode_number, width=width, height=height,
            humanreadable=humanreadable)
        barcode = base64.encodestring(barcode)
        self.barcode = barcode

    @api.depends('in_datetime', 'out_datetime')
    def _compute_attendance_state(self):
        for visitor in self:
            visitor.visitor_state = visitor.in_datetime and not visitor.out_datetime and 'checked_in' or 'checked_out'

    name = fields.Char(string="Number", readonly=True)
    visitor_name = fields.Char(string="Visitor Name")
    visitor_company_id = fields.Many2one('res.partner', required=False, string="Visitor Company")
    partner_id = fields.Many2one('hr.employee', string="Employee")
    in_datetime = fields.Datetime(string="Date Time In")
    out_datetime = fields.Datetime(string="Date Time Out")
    mobile_number = fields.Char(string="Phone/Mobile")
    email = fields.Char(string="Email")
    check = fields.Boolean("check")
    purpose = fields.Text(string="Reason")
    department_id = fields.Many2one('hr.department', string="Department")
    user_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user, string='Created By',
                              readonly=True)
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id,
                                 string='Company', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('exit', 'Exit'),
        ('cancel', 'Cancelled')], default='draft',
        track_visibility='onchange',
        copy=False, string="Status")
    image = fields.Binary("Image")
    signature = fields.Binary(string='Signature')
    barcode = fields.Binary(compute=get_barcode, string='Barcode', readonly=True, copy=False)
    barcode_number = fields.Char("Bar Code Number")
    student_name = fields.Many2one('visitor.student', string="Student Name", readonly=True)
    pin = fields.Char("Pin")
    visitor_state = fields.Selection(string="Attendance", compute='_compute_attendance_state',
                                     selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")])

    user_type = fields.Selection([
        ('user', 'Existing User'),
        ('new', 'New'),
    ], string="User Type")
    visitor_name_id = fields.Many2one('res.partner', 'Visitor Name')

    visit_type = fields.Selection([
        ('emp', 'Employee'),
        ('stu', 'Student'),
    ], string="Visit Type")

    check = fields.Boolean("Check")

    @api.multi
    def action_official_button(self):
        self.purpose = "Official"
        self.check = True

    @api.multi
    def action_pick_up_button(self):
        self.purpose = "Students Pick Up"
        self.check = True

    @api.multi
    def action_visitor_rel_button(self):
        self.purpose = "Visitor Relative"
        self.check = True

    
    @api.multi
    def action_confirm(self):
        attachment_ids = []

        self.state = 'confirm'
        if self.visit_type == 'emp':
            self.name = self.env['ir.sequence'].next_by_code('hr.visitor')
            random_number = ''.join(random.sample(map(chr, range(48, 57) + range(65, 90) + range(97, 122)), 7))
            if random:
                match = self.search([('barcode_number', '=', random_number)])
                if match:
                    random_number = ''.join(random.sample(map(chr, range(48, 57) + range(65, 90) + range(97, 122)), 7))
                    self.barcode_number = random_number
                else:
                    self.barcode_number = random_number
            self.pin = random.randint(1, 10000)
        if self.user_type == 'new':
            dic1 = {
                'name': self.visitor_name,
                'mobile': self.mobile_number,
                'visitor_check': True,
                'email': self.email,
                'image': self.image,
                'user_id': self.user_id.id,

            }
            self.env['res.partner'].create(dic1)



        template = self.env.ref('hr_visitor.visitor_mail_for_confirm_template')
        self.env['mail.template'].browse(template.id).sudo().send_mail(self.id, force_send=True)

    @api.multi
    def write(self, vals):
        """"give a unique alias name if given alias name is already assigned"""
        if vals.get('pin'):
            student_id = self.env['visitor.student'].search([('pin', '=', vals['pin'])])
            if student_id:

                vals['student_name'] = student_id.id
        return super(HrVisitorProcess, self).write(vals)

    @api.multi
    def action_check_in(self):
        self.state = 'check_in'
        self.in_datetime = datetime.now()

    @api.multi
    def action_check_out(self):
        self.state = 'check_out'
        self.out_datetime = datetime.now()


    @api.multi
    def action_exit(self):
        for record in self:
            record.state = 'exit'
            if record.out_datetime == False:
                raise ValidationError("Please Enter The Date Time Out.")

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'
        
    @api.multi
    def action_reset_to_draft(self):
        self.state = 'draft'

    @api.multi
    def print_visitor_card(self):
        if self.state == 'draft':
            raise ValidationError("You are not allow to print the visitor card in draft state.")

        return self.env['report'].get_action(self, 'hr_visitor.report_badge')
    
    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.department_id = self.partner_id.department_id.id

    @api.onchange('pin')
    def _onchange_pin(self):
        if self.pin:
            student_pin = self.env['visitor.student'].search([('pin', '=', self.pin)])
            if student_pin:
                self.student_name = student_pin.id
                self.check = True
                self.state = 'confirm'
                random_number = ''.join(random.sample(map(chr, range(48, 57) + range(65, 90) + range(97, 122)), 7))
                if random:
                    match = self.search([('barcode_number', '=', random_number)])
                    if match:
                        random_number = ''.join(
                            random.sample(map(chr, range(48, 57) + range(65, 90) + range(97, 122)), 7))
                        self.barcode_number = random_number
                    else:
                        self.barcode_number = random_number
            else:
                raise ValidationError("You have Enter the incorrect PIN ")


    @api.onchange('user_type', 'visitor_name_id')
    def onchange_user_type(self):
        if self.user_type == 'user':
            self.email = self.visitor_name_id.email
            self.mobile_number = self.visitor_name_id.mobile
            self.visitor_company_id = self.visitor_name_id.id

    @api.multi
    def action_email_button(self):
        template = self.env.ref('hr_visitor.visitor_mail_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)

    @api.multi
    def action_sms_button(self):

        # send SMS
        mobiles = []
        sms_obj = self.env['sms.config']

        mobiles.append(self.partner_id.mobile_phone)

        sms_ids = sms_obj.search([('active', '=', True)])
        if sms_ids:
            message = sms_ids.sms_body

        if sms_ids and mobiles:
            sms_rec = sms_ids
            url = str(sms_rec.url).strip()
            login = str(sms_rec.login).strip()
            password = str(sms_rec.password).strip()
            for mobile in mobiles:
                params = urllib.urlencode({
                    'user': login,
                    'password': password,
                    'sender': 'OpenERP',
                    'GSM': mobile,
                    'SMSText': message,
                })
                try:
                    request = urllib2.Request(url, params)
                    response = urllib2.urlopen(request)
                    result = response.read()
                except Exception, e:
                    pass
        return True


    @api.multi
    def print_button(self):

        return self.env['report'].get_action(self, 'hr_visitor.student_report')





class ResPartner(models.Model):
    _inherit ='res.partner'

    visitor_check = fields.Boolean('Visitor')
    visitor_count = fields.Integer("Visitor", compute='_compute_visitor_count')

    @api.multi
    def _compute_visitor_count(self):
        for partner in self:
            if partner:
                partner.visitor_count = self.env['hr.visitor'].search_count(
                    [
                        ('visitor_name', '=', partner.name),
                        ('mobile_number', '=', partner.mobile)
                    ])

    @api.multi
    def visitor_meeting(self):
        view_id = self.env.ref('hr_visitor.visitor_process_list').id
        context = self._context.copy()

        visitor_id = self.env['hr.visitor'].search(
            [
                ('visitor_name', '=', self.name),
                ('mobile_number', '=', self.mobile)
            ])
        return {
            'name': 'Visitor',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'hr.visitor',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', visitor_id.ids)],

        }


class HrDepartment(models.Model):
    _inherit ='hr.department'

    building_location = fields.Char("Building Location")

class MailTemplate(models.Model):
    _inherit = "mail.template"
    sms_body = fields.Text("SMS Body")




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
