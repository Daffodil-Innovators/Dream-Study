# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class DslStudyDocumentType(models.Model):
    _name = 'dsl.study.document.type'
    _description = 'Document Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(string='Active', default=True)
    note = fields.Text(string='Notes')
