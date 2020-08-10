import base64
import logging
import traceback
import os.path
from ast import literal_eval
from odoo import fields, models, api # pylint: disable=import-error

SUPPORTED_EXTENSIONS = ('xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx')
EMBEEDED_VIDEO_EXT = "oksvid"

_logger = logging.getLogger(__name__)

class IntranetDocument(models.Model):
    '''
    This is the base class INHERITED by all models in this module. It contains basic
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
    def compute_extensions(self):
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
        If the file is a Microsoft Office file (any file with a supported extension) it looks for its pdf
        representation and returns that instead.
        '''
        res = self.env[model].search([("id", "=", id)])[0]
        size = len(res.documents)
        if size > 0 and index < size:
            doc = res.documents[index]
            extension = doc.name[doc.name.index(".") + 1:]
            conv_enabled = self.env["ir.config_parameter"].sudo().get_param("oks_intranet.liboffice_convert")
            if conv_enabled and extension in SUPPORTED_EXTENSIONS:         
                try:
                    conversion = self.env["oks.intranet.conversion"].search([("model_name", "=", model.replace(".", "_")),
                        ("record_id", "=", id), ("file_name", "=", doc.name)])[0]
                    with open(conversion.conversion_path, "rb") as fl:
                        datas = base64.b64encode(fl.read())
                        return (doc.name, datas)
                except:
                    traceback.print_exc()
                    return -1
            elif extension == EMBEEDED_VIDEO_EXT:
                url = base64.b64decode(doc.datas).decode("UTF-8")
                return (doc.name, url)
            else:
                return (doc.name, doc.datas)
        else:
            return -1
            
    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")
    user_in_charge = fields.Many2one(string="Encargado", comodel_name="hr.employee", required=True)
    is_manual = fields.Boolean(string="Es manual", default=False)
    allowed_groups = fields.Many2many(comodel_name="res.groups", related="category.groups", store=False)
    date = fields.Date(string="Publicado", default=_get_today_date)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", required=True)
    documents = fields.Many2many(string="Documentos", comodel_name="ir.attachment")
    extensions = fields.Many2many(string="Extensiones de los archivos", readonly=True, compute=compute_extensions, store=True, comodel_name="oks.intranet.document.extension")

    def _set_attachment_data(self, record):
        for doc in record.documents:
            doc.res_id = record.id
        self.env.cr.commit()

    def _delete_unused_attachment(self, record):
        '''
        Odoo only deletes attachments linked to a record when the record itself is deleted. Deleting
        a file from the many2many binary widget won't delete the attachment. This method compares
        the attachments linked to the record with the attachments in the documents field and removes
        the ones that are not in the documents field.
        '''
        attachment_list =  self.env["ir.attachment"].search([('res_model', '=', record._name), 
            ('res_id', '=', record.id)])
        document_ids = record.documents.ids
        for attachment in attachment_list:
            if attachment.id not in document_ids:
                attachment.unlink()


    @api.model
    def create(self, vals):
        conv_enabled = self.env["ir.config_parameter"].sudo().get_param("oks_intranet.liboffice_convert")
        res = super(IntranetDocument, self).create(vals)
        self._set_attachment_data(res)
        if conv_enabled:
            self.env["oks.intranet.conversion"].compute_conversions({"model_name": res._name.replace(".", "_"),
                "record_id": res.id, "documents": res.documents})
        return res

    @api.multi
    def write(self, vals):
        '''
        The write method is overriden to perform any file conversions if necessary. This ensures that 
        file conversions are performed in any childs of this class too.
        '''
        conv_enabled = self.env["ir.config_parameter"].sudo().get_param("oks_intranet.liboffice_convert")
        model_name = self._name.replace(".", "_")
        conversion = self.env["oks.intranet.conversion"]
        res = super(IntranetDocument, self).write(vals)    
        if conv_enabled:
            for record in self:
                self._set_attachment_data(record)
                self._delete_unused_attachment(record)
                conversion.compute_conversions({"model_name": model_name, "record_id": record.id,
                    "documents": record.documents})
        return res

    @api.multi
    def unlink(self):
        '''
        Deletes all conversions attached with the record. Poor man's ondelete=cascade
        '''
        conversions = self.env["oks.intranet.conversion"]
        model_name = self._name.replace(".", "_")
        for record in self:
            conversions.drop_record({"model_name": model_name, "record_id": record.id})
        return super(IntranetDocument, self).unlink()   

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
