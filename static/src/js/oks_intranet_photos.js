// Loads image previews
odoo.define("oks_intranet.Photos", function(require) {
    "use strict";

    var Widget= require('web.Widget');
    var widgetRegistry = require('web.widget_registry');
    var FieldManagerMixin = require('web.FieldManagerMixin');
    var rpc = require("web.ajax");

    var MyWidget = Widget.extend(FieldManagerMixin, {
        template: "oks_intranet.PhotoPreview",
        init: function (parent, model, state) {
            this._super(parent);
            FieldManagerMixin.init.call(this);
        },
        start: function () {
            var imgDiv = this.$("#oks_intranet_img_div");
        },
        events: {
            "click #oks_back_btn": "back-evt",
        },
        "back-evt": function() {},
        "next-evt": function() {},
    });

    widgetRegistry.add(
        'oks_intranet_img_prev', MyWidget
    );
});