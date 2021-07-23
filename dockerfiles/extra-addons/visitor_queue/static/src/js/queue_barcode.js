odoo.define('visitor_queue.Kanbanviewes', function (require) {
"use strict";

var KanbanView = require('web_kanban.KanbanView');

KanbanView.include({
        init: function(parent, dataset, view_id, options) {
			var self = this;
			this._super.apply(this, arguments);
			if(parent.action && parent.action.auto_field > 0){
                self.refresh_interval = setInterval(_.bind(function(){
                        if(this.$el[0].clientWidth != 0){
                            console.log(this.$el[0].clientWidth)
                            this.do_reload();
                        }


                    }, self) , parent.action.auto_field*1000);
             }
	    },
    });

});
