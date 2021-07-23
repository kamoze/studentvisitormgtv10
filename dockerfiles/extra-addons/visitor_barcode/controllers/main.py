# -*- coding: utf-8 -*-
from odoo import fields, http, _
from odoo.http import request


class EventBarcode(http.Controller):

    @http.route('/visitor_barcode/open', type='json', auth="user")
    def register_attendee(self, barcode, **kw):
        admission_obj = request.env['hr.visitor']
        admission_rec = admission_obj.search([('barcode_number', '=', barcode)], limit=1)
        print ("sssssssssssssssssssssss", admission_rec)

        contractor_obj = request.env['visitor.contract']
        contractor_rec = contractor_obj.search([('barcode_number', '=', barcode)], limit=1)
        if not admission_rec or not contractor_rec:
            return {'warning': _('This barcode is not valid!')}
        if admission_rec:
            return {'admission_id': admission_rec.id}
        else:
            return {'admission_id': contractor_rec.id}

    @http.route(['/visitor_barcode/event'], type='json', auth="user")
    def get_event_data(self):
        return {
            'name': ''
        }
