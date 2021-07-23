from odoo import fields, models

class ParentInformation(models.Model):
 _name = 'parent.information'

 name =fields.Char("Name" ,required=True)
 image =fields.Binary("Image")
 occupation =fields.Char("Occupation",required=True)
 address =fields.Char("Address")
 phone = fields.Char("Phone", required=True)
 mobile = fields.Char("Mobile")
 email = fields.Char("Email",required=True)
 signature =fields.Binary("Signature")
 relationship = fields.Many2one('relationship.type',string="Relationship")
 parent_ids = fields.Many2many('visitor.student', 'rel_parents_students', 'parents_inforamtion_id', 'students_id',
                                string='Student/Ward')

