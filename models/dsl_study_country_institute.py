# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DslStudyCountryInstitute(models.Model):
    _name = 'dsl.study.country.institute'
    _description = 'Study Country Institute'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", readonly=True,)
    type = fields.Selection([('public', 'Public'), ('private', 'Private')],string="Type",required=True)
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    country_id = fields.Many2one('dsl.study.country',string="Country",ondelete="cascade")

    google_map = fields.Text(string="Google Map")
    address = fields.Text(string="Address")
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip = fields.Char(string="Zip")

    image_ids = fields.Many2many('ir.attachment','institute_ir_attachments_rel', string="Images",) 
    logo = fields.Image(string="Logo")
    note = fields.Text(string="Note")

    program_ids = fields.One2many('dsl.study.country.institute.program','institute_id',string="Programs")

    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name, country_id)', 'Institute name already exists in this country!'),
        ('code_unique', 'unique(code)', 'Code already exists!'),
    ]

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('dsl.study.country.institute')
        return super().create(vals)