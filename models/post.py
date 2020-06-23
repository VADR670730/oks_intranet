from odoo import models, fields, api # pylint: disable=import-error

class IntranetPost(models.Model):
    _name = "oks.intranet.post"
    _description = "Comunicado o notica de la intranet"

    @api.model
    def _get_today_date(self):
        return fields.Date.today()

    name = fields.Char(string="Titulo", required=True)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.post.category", required=True)
    description = fields.Char(string="Información")
    date = fields.Date(string="Publicado", readonly=True, default=_get_today_date)
    image = fields.Binary(string="Foto", attachment=True)

class IntranetPostCategory(models.Model):
    _name = "oks.intranet.post.category"

    name = fields.Char()

    _sql_constraints = [
        ('post_cat_uniq', 'UNIQUE (name)',  'No pueden existir dos categorias iguales')
    ]