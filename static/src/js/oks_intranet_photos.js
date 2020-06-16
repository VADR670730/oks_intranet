// Loads image previews
odoo.define("oks_intranet.Photos", function(require) {
    "use strict";

    var core = require("web.core");
    var Widget = require("web.Widget");

    var PreviewAction = Widget.extend({
        template: "oks_intranet.PhotoPreview",
        init: function(parent, value) {
            this._super(parent);
        },
        start: function() {
            
        },
    });

    core.action_registry.add("oks_photos_preview", PreviewAction);
});