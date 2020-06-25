/**
 * Extends kanban view to change the amount of records per page 
 */
odoo.define("oks_intranet.PostKanban", function(require) {
    var viewRegistry = require("web.view_registry");
    var KanbanModel = require("web.KanbanModel");
    var KanbanView = require("web.KanbanView");
    var HeightKanbanRenderer = require("oks_intranet.FullHeightKanbanRenderer");
    var KanbanController = require("web.KanbanController");

    /**
     * Need to also add align-content: start; so there is no huge
     * gap between rows where the view is not full
     */
    var CustomRenderer = HeightKanbanRenderer.extend({
        _render: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$el.css("align-content", "flex-start");               
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
            Renderer: CustomRenderer,
            Controller: KanbanController,
        }),
        init: function() {
            this._super.apply(this, arguments);
            this.loadParams.limit = 12;
        }
    });

    viewRegistry.add("oks_intranet_post_kanban", PhotoKanban)
});