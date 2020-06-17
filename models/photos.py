from odoo import models, fields, api # pylint: disable=import-error

class Photos(models.Model):
    _name = "oks.intranet.photos"
    _inherit = "oks.intranet.document"
    _description = "Album fotos intranet"

    @api.depends("documents")
    def _default_thumbnail(self):
        if len(self.documents) >= 1:
            return self.documents[0].datas

    @api.model
    def _default_category(self):
        return self.env.ref("oks_intranet.document_cat_general")

    @api.multi
    def get_doc_len(self):
        for record in self:
            return len(record.documents)

    @api.model
    def get_img64(self, index):
        size = len(self.documents)
        if size > 0 and index < size:
            return self.documents[index].datas 

    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", required=True, default=_default_category)
    thumbnail = fields.Binary(compute=_default_thumbnail, store=True)