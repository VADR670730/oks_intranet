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
    var KanbanRenderer = require("web.KanbanRenderer")
    var KanbanController = require("web.KanbanController");

    /**
     * This renderer can be used in all other kanban views where a masonry layout is required. It will 
     * always display two columns of records regardless of item length.
     */
    var PhotoRenderer = KanbanRenderer.extend({
        _render: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$el.css("height", "100%");
                var kanbans = self.$el.find(".oks_intranet_photo_kanban_cont")
                kanbans.each(function() {
                    
                });
            });
        },
    });

    /**
     * This view can be extended and have its loadParams.limit modified to a number that better
     * fits the model. It will still keep its masonry layout.
     */
    var PhotoKanban = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: KanbanModel,
            Renderer: PhotoRenderer,
            Controller: KanbanController,
        }),
        init: function() {
            this._super.apply(this, arguments);
            this.loadParams.limit = 6;
        }
    });

    viewRegistry.add("oks_intranet_photo_kanban", PhotoKanban)
});