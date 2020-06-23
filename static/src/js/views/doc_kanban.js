/**
 * Extends the kanban view and removes many2many tags' circles. 
 * It also injects css classes into said tags to make them look good.
 */

 odoo.define("oks_intranet.DocumentKanban", function(require) {
    var viewRegistry = require("web.view_registry");
    var KanbanModel = require("web.KanbanModel");
    var KanbanView = require("web.KanbanView");
    var KanbanRenderer = require("web.KanbanRenderer")
    var KanbanController = require("web.KanbanController");

    /**
     * This renderer can be used in all other kanban views where a masonry layout is required. It will 
     * always display two columns of records regardless of item length.
     */
    var DocRenderer = KanbanRenderer.extend({
        _render: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                var tagCont = self.$el.find(".o_kanban_tags");
                var tags = tagCont.find(".o_tag");
                tags.each(function(index) {
                    $(this).addClass("oks_intranet_ext_tag");
                    $(this).addClass("oks_intranet_ext_" + $(this).text());
                    $(this).find("span").remove();
                });
            });
        },
    });

    /**
     * This view can be extended and have its loadParams.limit modified to a number that better
     * fits the model. It will still keep its masonry layout.
     */
    var DocKanban = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: KanbanModel,
            Renderer: DocRenderer,
            Controller: KanbanController,
        }),
    });

    viewRegistry.add("oks_intranet_doc_kanban", DocKanban)
});