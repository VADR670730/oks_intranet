from odoo import models, fields, api # pylint: disable=import-error

'''
Used to display new's posts accessible by all users. Extends oks.intranet.document
and only adds a post_category field which is only used to organize and filter out
posts. Overwrites unused fields to erase them from the model.
'''
class IntranetPost(models.Model):
    _name = "oks.intranet.post"
    _inherits = "oks.intranet.document"
    _description = "Comunicado o notica de la intranet"

    @api.model
    def _default_category(self):
        return self.env.ref("oks_intranet.document_cat_general")

    post_category = fields.Many2one(comodel_name="oks.intranet.post.category", string="Categoría", required=True)

    # Overwrite unused fields inherited from model
    # No need to save this field anymore. It will always be the same.
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", default=_default_category, store=False)
    user_in_charge = fields.Many2one(store=False, required=False)
    is_manual = fields.Boolean(store=False)
    extensions = fields.Many2many(store=False)

class IntranetPostCategory(models.Model):
    _name = "oks.intranet.post.category"

    name = fields.Char()

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos categorias iguales')
    ]