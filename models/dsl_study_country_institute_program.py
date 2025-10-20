# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DslStudyCountryInstituteProgram(models.Model):
    _name = 'dsl.study.country.institute.program'
    _description = 'Institute Program'

    name = fields.Char(string="Program Name", required=True)
    code = fields.Char(string="Code", readonly=True)
    active = fields.Boolean(string="Active", default=True)
    number = fields.Char(string="Program Number")

    is_tuition_fee = fields.Boolean(string="Is Tuition Fee")
    tuition_fee = fields.Float(string="Tuition Fee")

    is_admission_fee = fields.Boolean(string="Is Admission Fee")
    admission_fee = fields.Float(string="Admission Fee")

    institute_id = fields.Many2one('dsl.study.country.institute',string="Institute",ondelete="cascade")

    note = fields.Text(string="Description")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Program name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('dsl.study.country.institute.program')
        res = super(DslStudyCountryInstituteProgram, self).create(vals)
        return res
    
    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active