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
            this.imgLen = null;
            this.imgSrc = null;
            this.imgName = null;
        },
        start: async function () {
            self = this;
            setTimeout(async function() { //Without this magical timeout the code runs before the view is rendered
                self.img = this.$("#oks_intranet_img");
                self.recordId = this.$("span[name='id']").text();
                if(!self.recordId) {
                    this.$("#oks_intranet_img_widget").hide();
                    return;
                }
                await self.img_len();
                if(self.imgLen <= 0) {
                    this.$("#oks_intranet_img_widget").hide();
                    return;
                }
                else if(self.imgLen == 1) {
                    this.$("#oks_img_btn_div").hide();
                }
                self.display_img();
            }, 1); 
        },
        events: {
            "click #oks_back_btn": "back-evt",
            "click #oks_next_btn": "next-evt",
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
                self.imgName = val[0];
                self.imgSrc = val[1];
                self.img.attr("src", "data:image/png;base64, " + self.imgSrc);
            });
        },
    });

    widgetRegistry.add(
        'oks_intranet_img_prev', MyWidget
    );
});