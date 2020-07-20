/**
 * Extends kanban view to change the amount of records per page 
 */
odoo.define("oks_intranet.PostKanban", function(require) {
    "use strict";
    var viewRegistry = require("web.view_registry");
    var KanbanModel = require("web.KanbanModel");
    var KanbanView = require("web.KanbanView");
    var KanbanRenderer = require("web.KanbanRenderer");
    var KanbanController = require("web.KanbanController");

    var KANBAN_POST_CLASS = "oks_intranet_post_kanban_cont";

    /**
     * t-afft-style should be able to do this directly on the kanban view
     * but it is not working. Hopefully this is just a temporary bandaid while I 
     * figure it out.
     */
    var PostRenderer = KanbanRenderer.extend({
        _render: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                self._rpc({model: "oks.intranet.post.category", method: "get_colors", args:[]}).then(function(val) {
                    var posts = self.$el.find("." + KANBAN_POST_CLASS);
                    posts.each(function(index) {
                        var cat = $(this).find(".oks_intranet_post_kanban_details").find("span")[0];
                        $(cat).css("background-color", val[$(cat).text()]);
                    });

                    var ghosts = self.$el.find(".o_kanban_ghost");
                    ghosts.each(function(index) {
                        $(this).addClass(KANBAN_POST_CLASS);
                    });
                });
                
            });
        }
    });

    /**
     * This view can be extended and have its loadParams.limit modified to a number that better
     * fits the model. It will still keep its masonry layout.
     */
    var PostKanban = KanbanView.extend({
        config: _.extend({}, KanbanView.prototype.config, {
            Model: KanbanModel,
            Renderer: PostRenderer,
            Controller: KanbanController,
        }),
        init: function() {
            this._super.apply(this, arguments);
            this.loadParams.limit = 12;
        }
    });

    viewRegistry.add("oks_intranet_post_kanban", PostKanban)
});