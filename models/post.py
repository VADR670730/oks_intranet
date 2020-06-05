# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IntranetPost(models.Model):
    _name = "oks.intranet.post"

    name = fields.Char(string="Titulo", required=True)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.post.category", required=True)
    description = fields.Char(string="Información")
    date = fields.Date(string="Publicado", readonly=True, default=fields.Date.today())
    image = fields.Binary(string="Foto", attachment=True)
    
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