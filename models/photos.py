from odoo import models, fields, api # pylint: disable=import-error

class Photos(models.Model):
    _name = "oks.intranet.photos"
    _inherit = "oks.intranet.document"
    _description = "Album fotos intranet"

    thumbnail = fields.Binary(string="Miniatura", attachment=True, store=True)

    @api.depends("documents")
    def _default_thumbnail(self):
        if len(self.documents) >= 1:
            return self.documents[0].datas

    @api.model
    def _default_category(self):
        return self.env.ref("oks_intranet.document_cat_general")

    # Overwrite unused fields inherited from model
    # No need to save this field anymore. It will always be the same.
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", default=_default_category, store=False)
    user_in_charge = fields.Many2one(store=False)
    is_manual = fields.Boolean(store=False)
    extensions = fields.Many2many(store=False)