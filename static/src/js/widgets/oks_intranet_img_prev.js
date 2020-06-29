/**
 * This Javascript widget works with all models that extend
 * oks.intranet.document. To properly work all the views
 * which use this widget must have two fields. They are usually
 * set as invisible.
 * 
 * The first field must be <field name="id"/>. This is so
 * the widget knows the id of the current record. 
 * 
 * Secondly the widget must know the model of the current
 * record. To do so it looks for a span with an id of "oks_intranet_model"
 * 
 * So in your view declare the following
 * <span id="oks_intranet_model">your.model.name</span>
 * 
 * The widget adds a "Preview files" button which upon click displays a modal
 * box with the files attached to the record. Currently it only works with images.
 */
odoo.define("oks_intranet.Photos", function(require) {
    "use strict";

    var Core = require("web.core");
    var Qweb = Core.qweb;
    var Widget= require("web.Widget");
    var widgetRegistry = require("web.widget_registry");

    var MyWidget = Widget.extend({
        template: "oks_intranet.PreviewButton",
        init: function (parent) {
            this._super(parent);
            this.fullWindow = null;
            this.index = 0;
            this.img = null;
            this.recordId = null;
            this.modelName = null;
            this.imgDiv = null;
            this.imgLen = null;
            this.imgSrc = null;
            this.imgName = null;
            this.pdfView = null;
        },
        start: async function () {
            self = this;
            setTimeout(async function() { //Without this magical timeout the code runs before the view is rendered
                self.recordId = $("span[name='id']").text();
                self.modelName = $("#oks_intranet_model").text();
                self.fullWindow = $("html");
                self.fullWindow.append(Qweb.render("oks_intranet.Preview"));
                self.imgDiv = $("#oks_intranet_prev_widget");
                self.imgName = $("#oks_intranet_prev_name");
                self.img = $("#oks_intranet_prev_img");
                self.pdfView = $("#oks_intranet_prev_pdf");
                self.pdfView.hide();

                //Add listeners to the buttons from the template rendered outside the widget
                //Unbind is an attempt to remove the weird double trigger that happens sometimes
                //I dont know if it actually works but it is better than nothing
                $("#oks_intranet_close_prev").unbind().click(function() { self.close_evt(); });       
                $("#oks_intranet_back_prev").unbind().click(function() { self.back_evt();});   
                $("#oks_intranet_next_prev").unbind().click(function() { self.next_evt();});   
                if(self.recordId) {
                    await self.img_len()
                    if (self.imgLen >= 1) {
                        $("#oks_intranet_prev_start").prop("disabled", false);
                    }
                }
            }, 1); 
        },
        events: {
            "click #oks_intranet_prev_start": "start-evt",
        },
        "start-evt": async function() {
            await this.display_img();
            this.imgDiv.css("display", "flex");
        },
        close_evt: async function() {
            this.imgDiv.hide();
        },
        back_evt: async function() {
            this.index--;
            if(this.index < 0) {
                this.index = this.imgLen - 1;
            }
            this.display_img();
        },
        next_evt: async function() {
            this.index++;
            if(this.index > (this.imgLen - 1)) {
                this.index = 0;
            }  
            this.display_img();
        },
        img_len: async function() {
            this.imgLen = await this._rpc({model: "oks.intranet.document", method: "get_doc_len",
            args: [this.recordId, this.modelName]}).then(function(val) {
                return val;
            });
        },
        display_img: async function() {
            self = this;
            await this._rpc({
                model: "oks.intranet.document", method: "get_img64",
                args: [this.recordId, this.modelName, this.index]}).then(function(val) {
                    var fileName = val[0].substring(0, 1).toUpperCase() + val[0].substring(1, val[0].indexOf("."));
                    if(val[0].substring(val[0].indexOf(".")) == ".pdf") {
                        self.pdfView.attr("src", "data:application/pdf;base64," + val[1]);
                        self.pdfView.attr("name", fileName);
                        self.img.hide();
                        self.imgName.hide();
                        self.pdfView.show();
                    }
                    else {
                        self.imgName.text(fileName);
                        self.imgSrc = val[1];
                        self.img.attr("src", "data:image/png;base64, " + self.imgSrc);
                        self.pdfView.hide();
                        self.imgName.show();
                        self.img.show();
                    }
            });
        },
    });

    widgetRegistry.add(
        'oks_intranet_file_preview', MyWidget
    );
});