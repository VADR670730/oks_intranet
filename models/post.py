from odoo import models, fields, api # pylint: disable=import-error

class IntranetPost(models.Model):   
    '''
    Used to display new's posts accessible by all users. Extends oks.intranet.document
    and adds a post_category field to filter aid in filtering. It also adds an HTML
    field used to display HTML content in it's form view. Its description is displayed
    in its kanban view and can only be seen by managers in its form view.
    '''
    _name = "oks.intranet.post"
    _inherit = "oks.intranet.document"
    _description = "Comunicado o notica de la intranet"
    _order = "date DESC"

    @api.model
    def _default_category(self):
        return self.env.ref("oks_intranet.document_cat_general")

    post_category = fields.Many2one(comodel_name="oks.intranet.post.category", string="Categoría", required=True)
    text_content = fields.Html(sanitize=False)

    # Overwrite unused fields inherited from model
    # No need to save this field anymore. It will always be the same.
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.document.category", default=_default_category, store=False)
    user_in_charge = fields.Many2one(store=False, required=False)
    is_manual = fields.Boolean(store=False)
    extensions = fields.Many2many(store=False)

class IntranetPostCategory(models.Model):
    '''
    Category that has no effect on record access. It is only meant as an organizational tool. The
    color is rendered by Javascript and used on Kanban views.
    '''
    _name = "oks.intranet.post.category"

    name = fields.Char(string="Nombre", required=True)
    color = fields.Char(string="Color", required=True, default="#808080")

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos categorias iguales')
    ]

    @api.model
    def get_colors(self):
        res = self.env["oks.intranet.post.category"].search([])
        retval = {}
        for record in res:
            retval[record.name] = record.color
        return retval
        