
from odoo import models, fields, api


class DslStudyCountry(models.Model):
    _name = 'dsl.study.country'
    _description = 'Study Country'

    country_id = fields.Many2one('res.country', string="Country", required=True)
    name = fields.Char(related='country_id.name', string="Country Name", store=True, readonly=True)
    code = fields.Char(string="Code", readonly=True)
    active = fields.Boolean(string="Active", default=True)

    responsible_person = fields.Many2many('res.users', string="Responsible Person", required=True, store=True)
    institute_ids = fields.One2many('dsl.study.country.institute', 'country_id', string="Institutes")

    is_security_money = fields.Boolean(string="Is Security Money")
    security_money = fields.Float(string="Security Money")

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    note = fields.Text(string="Note")

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name already exists!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('dsl.study.country')
        return super().create(vals)

    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active