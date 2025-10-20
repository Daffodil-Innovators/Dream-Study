from odoo import models, fields, api

class DslStudySource(models.Model):
    _name = 'dsl.study.source'
    _description = 'DSL Study Source'

    name = fields.Char(string="Name",required=True)
    code = fields.Char(string="Code")
    active = fields.Boolean(string="Active", default=True)
    note = fields.Text(string="Note")


    sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('dsl.study.source')
        return super().create(vals)
    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active