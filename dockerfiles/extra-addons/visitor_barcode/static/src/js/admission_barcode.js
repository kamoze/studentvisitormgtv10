odoo.define('visitor_barcode.EventScanView', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');
var Session = require('web.session');
var Notification = require('web.notification').Notification;
var NotificationManager = require('web.notification').NotificationManager;
var BarcodeHandlerMixin = require('barcodes.BarcodeHandlerMixin');
var time = require('web.time');
var Model = require('web.Model');


var QWeb = core.qweb;
var _t = core._t;

// Success Notification with thumbs-up icon
var Success = Notification.extend({
    template: 'event_barcode_success'
});

var NotificationSuccess = NotificationManager.extend({
    success: function(title, text, sticky) {
        return this.display(new Success(this, title, text, sticky));
    }
});

// load widget with main barcode scanning View
var EventScanView = Widget.extend(BarcodeHandlerMixin, {
    template: 'event_barcode_template',
    events: {
        'click .o_pin_success_button': 'on_manual_scan',
        'click .o_hr_attendance_pin_pad_button_0': 'open_0',
        'click .o_hr_attendance_pin_pad_button_1': 'open_1',
        'click .o_hr_attendance_pin_pad_button_2': 'open_2',
        'click .o_hr_attendance_pin_pad_button_3': 'open_3',
        'click .o_hr_attendance_pin_pad_button_4': 'open_4',
        'click .o_hr_attendance_pin_pad_button_5': 'open_5',
        'click .o_hr_attendance_pin_pad_button_6': 'open_6',
        'click .o_hr_attendance_pin_pad_button_7': 'open_7',
        'click .o_hr_attendance_pin_pad_button_8': 'open_8',
        'click .o_hr_attendance_pin_pad_button_9': 'open_9',
        'click .o_hr_attendance_pin_pad_button_C': 'open_c',
        'click .o_hr_attendance_pin_pad_button_ok': 'open_ok',
    },

    init: function(parent, action) {
        BarcodeHandlerMixin.init.call(this, parent, action);
        this._super.apply(this, arguments);
        this.action = action;
        this.parent = parent;
    },
    willStart: function() {
        var self = this;
        return this._super().then(function() {
            return Session.rpc('/visitor_barcode/event', {
                event_id: self.action.context.active_id
            }).then(function(result) {
                self.data = self.prepare_data(result);
            });
        });
    },
    start: function() {
        var self = this;
        this.notification_manager = new NotificationSuccess();
        this.notification_manager.appendTo(self.parent.$el);
        this.updateCount(
            self.$('.o_event_reg_attendee'),
            self.data.count
        );
    },
    prepare_data: function(result) {
        var start_date = moment(time.auto_str_to_date(result.start_date));
        var end_date = moment(time.auto_str_to_date(result.end_date));
        var localedata = start_date.localeData();
        result['date'] =  start_date.date() === end_date.date() ? start_date.date() : _.str.sprintf("%s - %s", start_date.date(), end_date.date());
        result['month'] = start_date.month() === end_date.month() ? localedata._months[start_date.month()] : _.str.sprintf('%s - %s', localedata._monthsShort[start_date.month()], localedata._monthsShort[end_date.month()]);
        return result;
    },
    on_manual_scan: function(e) {
        var barcode = $("#event_barcode").val();

        if (barcode){

            if (e.which === 1) { // Enter
                var value = $(e.currentTarget).val().trim();
                if(value) {
                    this.on_barcode_scanned(value);
                    $(e.currentTarget).val('');
                } else {
                    this.do_warn(_t('Error'), _t('Invalid user input'));
                }
            }
        }
        else {

             this.do_warn(_t('Error'), _t('Please Enter the barcode'));

        }
    },
    on_attach_callback: function() {
        this.start_listening();
    },
    on_detach_callback: function() {
        this.stop_listening();
    },
    on_barcode_scanned: function(barcode) {
        var badge_id = $("#event_barcode").val();

           var self = this
           var list1 = []
            var list2 = []

            var productivity_domain = [['barcode_number', '=',badge_id ]];

            new Model('hr.visitor').call('search_read', [productivity_domain, []]).then(function(result) {
             _.each(result, function(data) {
             if (data){
                    list1.push(data.state)
                    list1.push(data.pin)
                    list1.push(data.visitor_name)
                    list1.push(data.id)
                    list1.push(data.in_datetime)
                    list1.push(data.out_datetime)
                    list1.push(data.user_type)
                    list1.push(data.visitor_name)
                    list1.push(data.visitor_name_id)
                    }
             else   {

                             alert('Please enter the valid barcode')

             }
                });
                if (list1[4] && list1[5]){
                alert('Already Signed In/Out, please create another entry')
                }
                else{
                    self.$el.html(QWeb.render("VisitorKioskConfirm", {widget: list1 }));
                }
             });

             new Model('visitor.contract').call('search_read', [productivity_domain, []]).then(function(result) {
             _.each(result, function(data) {
                list2.push(data.state)
                list2.push(data.pin)
                list2.push(data.id)
                list2.push(data.check_in)
                list2.push(data.check_out)

                });

             if (list2){

                self.$el.html(QWeb.render("VisitorKioskConfirm", {widget: list2 }));
                }

             });
    },
    open_0: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 0);
    },
     open_1: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 1);
    },
     open_2: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 2);
    },
     open_3: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 3);
    },
     open_4: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 4);
    },
     open_5: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 5);
    },
     open_6: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 6);
    },
     open_7: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 7);
    },
     open_8: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 8);
    },
     open_9: function() {
         this.$('.o_hr_attendance_PINbox').val(this.$('.o_hr_attendance_PINbox').val() + 9);
    },

     open_c: function() {
            this.$('.o_hr_attendance_PINbox').val('');    },

     open_ok: function() {


           var self = this;
           var visitor_id = $("#event_parse").val();
           if (visitor_id){
            this.$('.o_hr_attendance_pin_pad_button_ok').attr("disabled", "disabled");
                var hr_employee = new Model('hr.visitor');
                hr_employee.call('attendance_manual', [[Number(visitor_id)], this.next_action, this.$('.o_hr_attendance_PINbox').val()])
                .then(function(result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.do_warn(result.warning);
                        setTimeout( function() { self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled"); }, 500);
                    }
                });
             }

            var contract_id = $("#contractor_parse").val();

            if (contract_id){

            var visitor_contract = new Model('visitor.contract');
            visitor_contract.call('attendance_manual', [[Number(contract_id)], this.next_action, this.$('.o_hr_attendance_PINbox').val()])
            .then(function(result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
                    setTimeout( function() { self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled"); }, 500);
                }
            });


             }
             },



    open_event_form: function() {
        this.do_action({
            name: 'Admission',
            type: 'ir.actions.act_window',
            res_model: 'hr.visitor',
            views: [[false, 'form'], [false, 'kanban'], [false, 'calendar'], [false, 'list']],
            res_id: this.action.context.active_id,
        });
    },
    updateCount: function(element, count) {
        element.html(count);
    }
});

core.action_registry.add('even_barcode.scan_view', EventScanView);

return {
    Success: Success,
    NotificationSuccess: NotificationSuccess,
    EventScanView: EventScanView
};

});
