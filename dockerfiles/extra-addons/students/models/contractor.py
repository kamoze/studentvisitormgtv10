from odoo import fields, models,api
from datetime import datetime
import random
import base64

class VisitorContract(models.Model):
    _name = 'visitor.contract'
    _rec_name = 'project_type_id'

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

    @api.depends('check_in', 'check_out')
    def _compute_attendance_state(self):
        for contract in self:
            contract.visitor_state = contract.check_in and not contract.check_out and 'checked_in' or 'checked_out'

    sequence_number = fields.Char('Number', readonly=True)
    badge_ids = fields.Many2many('work.location', 'rel_badge_work', 'badge_work', 'work_id' ,string="Badge")
    project_type_id = fields.Many2one('project.project', "Project Name")
    check_in = fields.Datetime("Check In")
    check_out = fields.Datetime("Check Out")
    contractor_name_id = fields.Many2one('res.partner', string="Contractor Name")
    company_name_id = fields.Many2one('res.company', string="Company Name")
    pin = fields.Char(string="PIN")
    barcode_number = fields.Char("Barcode Number")
    barcode = fields.Binary(compute=get_barcode, string='Barcode', readonly=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),], default='draft',
        track_visibility='onchange',
        copy=False, string="Status")
    user_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user, string='Created By', readonly=True)
    visitor_state = fields.Selection(string="Attendance", compute='_compute_attendance_state', selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")])
    image = fields.Binary('Image')
    sequence_number = fields.Char('Number', readonly=True)


    @api.multi
    def action_confirm_check_in(self):
        self.check_in = datetime.now()
        self.state = 'check_in'

    @api.multi
    def action_confirm_check_out(self):
        self.check_out = datetime.now()
        self.state = 'check_out'

    @api.multi
    def action_confirm(self):
        random_number = ''.join(random.sample(map(chr, range(48, 57) + range(65, 90) + range(97, 122)), 7))
        self.barcode_number = random_number
        self.state = 'confirm'

    @api.model
    def create(self, vals):
        Number = self.env.ref('students.sequence_number_id')
        vals['sequence_number'] = Number.next_by_id()
        return super(VisitorContract, self).create(vals)

    @api.multi
    def pin_generate(self):
        random_number = ''.join(random.sample(map(chr, range(49, 57)), 4))
        self.pin = random_number
        return random_number

    @api.multi
    def print_badge(self):
        return self.env['report'].get_action(self, 'students.badge_report')


class Project(models.Model):
    _inherit = "project.project"

    project_team_member_ids = fields.Many2many('hr.employee','rel_employee_team','team_id','employee_id', string="Project Team Member")
    project_start_date = fields.Datetime("Project Start Date")
    estimate_end_date = fields.Datetime("Estimate End Date")

