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
                self._rpc({model: "oks.intranet.photos", method: "get_img64", args: [self.recordId, 0]}).then(function(returned_value) {
                    var img = $("<img />")
                    img.attr("src", "data:image/png;base64, " + returned_value);
                    img.appendTo(self.imgDiv);
                });
            }, 150); 
        },
        events: {
            "click #oks_back_btn": "back-evt",
            "click #oks_next_btn": "next-evt",
        },
        "back-evt": function() {
            this.index++;
            console.log(this.index);
        },
        "next-evt": function() {
            this.index++;
            console.log(this.index);
        },
    });

    widgetRegistry.add(
        'oks_intranet_img_prev', MyWidget
    );
});