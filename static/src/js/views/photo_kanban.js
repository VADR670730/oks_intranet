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
    var KanbanRenderer = require("web.KanbanRenderer");
    var KanbanController = require("web.KanbanController");

    var PhotoRenderer = KanbanRenderer.extend({
        _render: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                    var ghosts = self.$el.find(".o_kanban_ghost");
                    ghosts.each(function(index) {
                        $(this).addClass("oks_intranet_photo_kanban_cont");
                    });
                });
        }
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