// Loads image previews
odoo.define("oks_intranet.Photos", function(require) {
    "use strict";

    var Widget= require('web.Widget');
    var widgetRegistry = require('web.widget_registry');

    var MyWidget = Widget.extend({
        template: "oks_intranet.PhotoPreview",
        init: function (parent) {
            this._super(parent);
            this.index = 0;
        },
        start: function () {
            self = this;
            setTimeout(function() { 
                self.imgDiv = this.$("#oks_intranet_img_div");
                self.recordId = this.$("span[name='id']").text();
                self.update_count();
            }, 1000); 
        },
        events: {
            "click #oks_back_btn": "back-evt",
        },
        "back-evt": function() {},
        "next-evt": function() {},
        
        update_count: function() {
            self = this;
            self._rpc({
                model: 'oks.intranet.photos',
                method: 'get_doc_len',
                args: [self.recordId]
                }).then(function (returned_value) { 
                    self.imgCount = returned_value; 
                });
        },

        display_image: function(index) {
            
        },
    });

    widgetRegistry.add(
        'oks_intranet_img_prev', MyWidget
    );
});