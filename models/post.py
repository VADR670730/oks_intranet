from odoo import models, fields, api # pylint: disable=import-error

class IntranetPost(models.Model):
    _name = "oks.intranet.post"
    _description = "Comunicado o notica de la intranet"

    @api.model
    def _get_today_date(self):
        return fields.Date.today()

    @api.model
    def _compute_dev_view(self):
            if self.env.user.has_group("oks_intranet.intranet_manager"):
                return True
            else:
                return False

    name = fields.Char(string="Titulo", required=True)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.post.category", required=True)
    category_name = fields.Char(related="category.name", store=False, readonly=True)
    description = fields.Char(string="Información")
    date = fields.Date(string="Publicado", readonly=True, default=_get_today_date)
    image = fields.Binary(string="Foto", attachment=True)
    dev_view = fields.Boolean(default=_compute_dev_view, store=False)

    @api.model
    def create(self, vals):
        result = super(IntranetPost, self).create(vals)
        return result

class IntranetPostCategory(models.Model):
    _name = "oks.intranet.post.category"

    name = fields.Char()

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos categorias iguales')
    ]