from odoo import fields, models

class BadgeConfiguration(models.Model):
    _name = 'work.location'
    _rec_name = 'work_location_id'

    work_location_id = fields.Many2one('visitor.location',"Work Location")
    floor = fields.Char("Floor")


class VisitorLocation(models.Model):
    _name = 'visitor.location'
    _rec_name = 'name'

    name = fields.Char("Name")



