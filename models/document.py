from odoo import fields, models, api # pylint: disable=import-error

class Document(models.Model):
    _name = "oks.intranet.document"
    _description = "Documento de intranet"

    @api.model
    def _get_today_date(self):
        return fields.Date.today()

    @api.multi
    def _get_user_group(self):
        module_id = self.env["ir.module.category"].search([("name", "=", "Intranet")]).id
        user_id = self.env.user.id

    name = fields.Char(required=True)
    description = fields.Char()
    is_manual = fields.Boolean(default=False)
    user_group = fields.Many2many(comodel_name="res.groups", compute=_get_user_group)
    allowed_group = fields.Many2many(comodel_name="res.groups", related="category.groups")
    date = fields.Date(string="Publicado", readonly=True, default=_get_today_date)
    category = fields.Many2one(comodel_name="oks.intranet.document.category", required=True)
    document = fields.Binary(attachment=True)


class DocumentCategory(models.Model):
    _name = "oks.intranet.document.category"

    name = fields.Char()
    groups = fields.Many2many("res.groups", required=True)