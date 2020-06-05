from odoo import models, fields, api

class IntranetPost(models.Model):
    _name = "oks.intranet.post"

    @api.model
    def _get_today_date(self):
        return fields.Date.today()

    @api.multi
    def _compute_category_name(self):
        for record in self:
            record.category_name = record.category.name

    @api.multi
    def _compute_dev_view(self):
        for record in self:
            if self.env.user.has_group("oks_intranet.intranet_manager"):
                record.dev_view = True
            else:
                record.dev_view = False

    name = fields.Char(string="Titulo", required=True)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.post.category", required=True)
    category_name = fields.Char(compute=_compute_category_name, store=False)
    description = fields.Char(string="Información")
    date = fields.Date(string="Publicado", readonly=True, default=_get_today_date)
    image = fields.Binary(string="Foto", attachment=True)
    dev_view = fields.Boolean(compute=_compute_dev_view, store=False)

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