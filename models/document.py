from odoo import fields, models, api # pylint: disable=import-error

class Document(models.Model):
    _name = "oks.intranet.document"
    _description = "Documento de intranet"

    @api.model
    def _get_today_date(self):
        return fields.Date.today()

    name = fields.Char(string="Nombre", required=True)
    description = fields.Char(string="Descripción")
    is_manual = fields.Boolean(string="Es manual", default=False)
    allowed_groups = fields.Many2many(comodel_name="res.groups", related="category.groups", store=False)
    date = fields.Date(string="Publicado", readonly=True, default=_get_today_date)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", required=True)
    category_name = fields.Char(string="Categoria", related="category.name", store=False, readonly=True)
    documents = fields.Many2many(string="Documentos", comodel_name="ir.attachment")


class DocumentCategory(models.Model):
    _name = "oks.intranet.document.category"

    @api.model
    def _get_category(self):
        return self.env.ref("oks_intranet.intranet_management").id

    name = fields.Char(required=True)
    category_id = fields.Many2one(comodel_name="ir.model.category", default=_get_category, store=False)
    groups = fields.Many2many(comodel_name="res.groups", required=True)