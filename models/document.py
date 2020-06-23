import os.path
from ast import literal_eval
from odoo import fields, models, api # pylint: disable=import-error

class Document(models.Model):
    _name = "oks.intranet.document"
    _description = "Documento de intranet"

    @api.model
    def _get_today_date(self):
        return fields.Date.today()

    @api.depends("documents")
    def compute_docs(self):
        ext = self.env["oks.intranet.document.extension"].search([])
        for record in self:
            ext_ids = set()
            for doc in record.documents:
                doc_ext = os.path.splitext(doc.name)[1][1:]
                for ex in ext:
                    if doc_ext == ex.name:
                        ext_ids.add(ex.id)
            record.extensions = [(6, 0, ext_ids)]
            
    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    user_in_charge = fields.Many2one(string="Encargado", comodel_name="hr.employee", required=True)
    is_manual = fields.Boolean(string="Es manual", default=False)
    allowed_groups = fields.Many2many(comodel_name="res.groups", related="category.groups", store=False)
    date = fields.Date(string="Publicado", readonly=True, default=_get_today_date)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", required=True)
    documents = fields.Many2many(string="Documentos", comodel_name="ir.attachment")
    extensions = fields.Many2many(string="Extensiones de los archivos", readonly=True, compute=compute_docs, store=True, comodel_name="oks.intranet.document.extension")


class DocumentCategory(models.Model):
    _name = "oks.intranet.document.category"

    @api.model
    def _get_category(self):
        return self.env.ref("oks_intranet.intranet_management").id

    name = fields.Char(required=True)
    category_id = fields.Many2one(comodel_name="ir.module.category", default=_get_category, store=False)
    groups = fields.Many2many(comodel_name="res.groups", required=True)

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos categorias iguales')
    ]

class ExtensionTag(models.Model):
    _name = "oks.intranet.document.extension"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos extensiones iguales')
    ]
