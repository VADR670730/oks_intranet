import os.path
from ast import literal_eval
from odoo import fields, models, api # pylint: disable=import-error

class Document(models.Model):
    '''
    This is the base class INHERITED by all models in this model. It contains basic
    functionality to restrict access to records based on category and most importantly, 
    it interacts with the oks_intranet_img_prev widget which uses XMLRPC calls to send
    the documents' base64 content to the javascript client so that they can be rendered
    and seen by the user without having to donwload the file to their computer.
    '''
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

    @api.model
    def get_doc_len(self, id, model):
        res = self.env[model].search([("id", "=", id)])[0]
        return len(res.documents)

    @api.model
    def get_img64(self, id, model, index):
        '''
        Method called by the Javascript preview widget. It returns the base64 binary content of the attachment.
        '''
        res = self.env[model].search([("id", "=", id)])[0]
        size = len(res.documents)
        if size > 0 and index < size:
            return (res.documents[index].name, res.documents[index].datas)
        else:
            return -1
            
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
    '''
    This model is used to filter access to oks.intranet.document records based on the group
    or category assigned to them. The groups this model can contain should be groups that
    belong to this module. 
    '''
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
    '''
    Model used to retrieve all the extensions included in the attached documents of oks.intranet.document records.
    This information is displayed ONLY in oks.intranet.document kanban views.
    '''
    _name = "oks.intranet.document.extension"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos extensiones iguales')
    ]
