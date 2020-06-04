# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IntranetPost(models.Model):
    _name = "oks.intranet.post"

    name = fields.Char(string="Titulo", required=True)
    category = fields.Many2one(string="Categoria", comodel_name="oks.intranet.post.category", required=True)
    date = fields.Date(string="Publicado", readonly=True)
    image = fields.Many2many(comodel_name="ir.attachment")
    
    @api.model
    def create(self, vals):
        result = super(IntranetPost, self).create(vals)
        return result

class IntranetPostCategory(models.Model):
    _name = "oks.intranet.post.category"

    name = fields.Char()