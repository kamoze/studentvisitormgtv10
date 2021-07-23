from odoo import models, fields, api, exceptions, _, SUPERUSER_ID


class HrEmployee(models.Model):
    _inherit = "hr.visitor"

    @api.multi
    def _check_color(self):
        res = {}
        color = 0
        for record in self:
            if record.state == 'confirm':
                color = 1

            res[record.id] = color
        return res

    member_color = fields.Integer(compute=_check_color)





class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    auto_field = fields.Integer("Auto")
