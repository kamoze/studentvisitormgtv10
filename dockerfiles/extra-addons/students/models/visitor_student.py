from odoo import models, fields, api
import random

class VisitorStudent(models.Model):
    _name = 'visitor.student'

    name = fields.Char(string="Name")
    image = fields.Binary("Image")
    class_id = fields.Many2one('visitor.school',string="Class")
    school_id = fields.Many2one('visitor.class',string="School")
    arm = fields.Char("ARM")
    pin = fields.Char(change_default=True ,string="PIN")
    date_of_entry = fields.Date("Date of Entry")
    student_ids = fields.Many2many('parent.information', 'rel_student_parent', 'student_id', 'parent_id',
                                  string='Parent')


    @api.multi
    def pin_generate(self):
        random_number = ''.join(random.sample(map(chr,range(49, 57)), 4))
        exits_no = self.search([('pin', '=', random_number)])
        if exits_no:
            random_number = ''.join(random.sample(map(chr, range(49, 57)), 4))
            self.pin = random_number
        self.pin = random_number
        return random_number


class VisitorClass(models.Model):
    _name = 'visitor.class'

    name = fields.Char("Name")

class VisitorSlass(models.Model):
    _name = 'visitor.school'

    name = fields.Char("Name")

class RelationshipType(models.Model):
    _name = 'relationship.type'

    name = fields.Char("Name")



