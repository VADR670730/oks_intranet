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

    @api.model
    def get_doc_len(self, id):
        res = self.env["oks.intranet.photos"].search([("id", "=", id)])[0]
        return len(res.documents)


    @api.model
    def get_img64(self, id, index):
        res = self.env["oks.intranet.photos"].search([("id", "=", id)])[0]
        size = len(res.documents)
        if size > 0 and index < size:
            return (res.documents[index].name, res.documents[index].datas)
        else:
            return -1

    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", required=True, default=_default_category)
    thumbnail = fields.Binary(compute=_default_thumbnail, store=True)

    #Overwrite unused fields inherited from model
    user_in_charge = fields.Many2one(store=False)
    is_manual = fields.Boolean(store=False)