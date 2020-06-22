/**
 * This Javascript code declares a widget that is referenced in photo views. Said
 * widget displays the images contained in the documents (many2many ir.attachment) field
 * of oks.intranet.photos
 * 
 * To do this it gathers the current record id from a hidden field in the view and keeps
 * track of the index or element displayed. The back and next buttons change said index.
 * 
 * The image is displayed by calling a method on the python class which returns the
 * base64 encoded datas field from ir.attachment, said data is set as the src for
 * the HTML img element.
 */
odoo.define("oks_intranet.Photos", function(require) {
    "use strict";

    var Widget= require('web.Widget');
    var widgetRegistry = require('web.widget_registry');

    var MyWidget = Widget.extend({
        template: "oks_intranet.PhotoPreview",
        init: function (parent) {
            this._super(parent);
            this.index = 0;
            this.img = null;
            this.recordId = null;
            this.imgDiv = null;
            this.imgLen = null;
            this.imgSrc = null;
            this.imgName = null;
        },
        start: async function () {
            self = this;
            setTimeout(async function() { //Without this magical timeout the code runs before the view is rendered
                self.recordId = this.$("span[name='id']").text();
                self.imgName = this.$("#oks_intranet_img_name");
                self.img = this.$("#oks_intranet_img");
                self.imgDiv = this.$("#oks_intranet_img_widget");
                self.imgDiv.hide();
                await self.img_len();
                if(!self.recordId || self.imgLen <= 0) {
                    this.$("#oks_intranet_prev_start").prop("disabled", true);
                }
            }, 1); 
        },
        events: {
            "click #oks_intranet_prev_start": "start-evt",
            "click #oks_back_btn": "back-evt",
            "click #oks_next_btn": "next-evt",
        },
        "start-evt": async function() {
            this.display_img();
            this.imgDiv.show();
            this.$("#oks_intranet_prev_start").remove();
        },
        "back-evt": async function() {
            await this.img_len();
            this.index--;
            if(this.index < 0) {
                this.index = this.imgLen - 1;
            }
            this.display_img();
        },
        "next-evt": async function() {
            await this.img_len();
            this.index++;
            if(this.index > (this.imgLen - 1)) {
                this.index = 0;
            }  
            this.display_img();
        },
        img_len: async function() {
            this.imgLen = await this._rpc({model: "oks.intranet.photos", method: "get_doc_len", args: [this.recordId]}).then(function(val) {
                return val;
            });
        },
        display_img: async function() {
            self = this;
            await this._rpc({model: "oks.intranet.photos", method: "get_img64", args: [this.recordId, this.index]}).then(function(val) {
                self.imgName.text(val[0].substring(0, 1).toUpperCase() + val[0].substring(1, val[0].indexOf(".")));
                self.imgSrc = val[1];
                self.img.attr("src", "data:image/png;base64, " + self.imgSrc);
            });
        },
    });

    widgetRegistry.add(
        'oks_intranet_img_prev', MyWidget
    );
});