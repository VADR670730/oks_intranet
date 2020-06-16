from odoo import models, fields, api # pylint: disable=import-error

class Photos(models.Model):
    _name = "oks.intranet.photos"
    _inherit = "oks.intranet.document"
    _description = "Album fotos intranet"

    @api.onchange("documents")
    def _compute_img_len(self):
        self.img_len = len(self.documents)

    @api.onchange("documents")
    def _compute_img(self):
        if self.img_len >= 1:
            self.display_img = self.documents[0].datas
        else:
            self.display_img = self.env.ref("project.msg_task_data_14_attach").datas

    @api.model
    def _default_category(self):
        return self.env.ref("oks_intranet.document_cat_general")

    def action_img_back(self):
        if self.img_len >= 1:
            if (self.display_index - 1) >= 0:
                self.display_index -= 1
            else:
                self.display_index = self.img_len - 1
            self.display_img = self.documents[self.display_index].datas

    def action_img_next(self):
        if self.img_len >= 1:
            if(self.display_index + 1) < self.img_len:
                self.display_index += 1
            else:
                self.display_index = 0
            self.display_img = self.documents[self.display_index].datas

    img_len = fields.Integer(store=False, compute=_compute_img_len)
    display_index = fields.Integer(store=False, default=0)
    display_img = fields.Binary(compute=_compute_img, readonly=True, store=False)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", required=True, default=_default_category)