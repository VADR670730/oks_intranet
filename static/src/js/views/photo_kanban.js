/**
 * Basic renderer used just to make kanban viewports take up the whole
 * height of their container. Used by post and photo kanban views.
 */
odoo.define("oks_intranet.FullHeightKanbanRenderer", function(require) {
    "use strict";

    var KanbanRenderer = require("web.KanbanRenderer");
    var FullHeightKanban = KanbanRenderer.extend({
        _render: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$el.css("height", "100%");               
            });
        },
    });

    return FullHeightKanban;
});


/**
 * Kanban views do not take the whole screen height automatically.
 * I am too scared to change overwrite the css class and make 
 * all kanban views do it so instead I create this custom view
 * to inject the style attributes and also to limit the size of 
 * records per page to 6.
 */
odoo.define("oks_intranet.PhotoKanban", function(require) {
    var viewRegistry = require("web.view_registry");
    var KanbanModel = require("web.KanbanModel");
    var KanbanView = require("web.KanbanView");
    var HeightKanbanRenderer = require("oks_intranet.FullHeightKanbanRenderer");
    var KanbanController = require("web.KanbanController");

   

    /**
     * This view can be extended and have its loadParams.limit modified to a number that better
     * fits the model. It will still keep its masonry layout.
     */
    var PhotoKanban = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: KanbanModel,
            Renderer: HeightKanbanRenderer,
            Controller: KanbanController,
        }),
        init: function() {
            this._super.apply(this, arguments);
            this.loadParams.limit = 6;
        }
    });

    viewRegistry.add("oks_intranet_photo_kanban", PhotoKanban)
});