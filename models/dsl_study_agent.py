# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class DslStudyAgent(models.Model):
    _name = 'dsl.study.agent'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'first_name'
    _description = 'Agent Profile'

    ###############################
    ###### Profile Information ####
    ###############################
    agent_id = fields.Char(string='Agent Id')
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    photo = fields.Image()
    email = fields.Char(string='Email')
    phone_number = fields.Char(string='Phone')
    skype_id = fields.Char(string='Skype')
    whatsapp_id = fields.Char(string='Whatsapp')
    nid = fields.Char(string='NID')
    account_manager_id = fields.Many2one('res.users', string='Account Manager')  # placeholder
    agent_code = fields.Char(string='Agent Code', readonly=True, copy=False, default='New')
    note=fields.Text(string='Notes')
    name = fields.Char(string="Full Name", compute="_compute_name", store=True)

    ###############################
    ###### Company Information ####
    ###############################
    company_logo = fields.Image()
    company_name = fields.Char(string='Company Name')
    website = fields.Char(string='Website Link')
    main_source_of_students = fields.Many2many('res.country', string='Main Source Of Education')
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state = fields.Char(string='State')
    postal_code = fields.Char(string='Postal Code/Zip')
    business_certificate = fields.Binary(string='Business Certificate')
    country = fields.Many2one('res.country', string='Country')

    ###############################
    ###### Business Social ########
    ###############################
    facebook = fields.Char(string='Facebook')
    instagram = fields.Char(string='Instagram')
    linkedin = fields.Char(string='Linkedin')
    twitter = fields.Char(string='Twitter')

    ###############################
    ###### Status / Workflow ######
    ###############################
    stage = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ], string='Status', default='pending', tracking=True)

    sl = fields.Char(string='SL', compute='_compute_sl')


    @api.model
    def create(self, vals):
        if vals.get('agent_code', 'New') == 'New':
            vals['agent_code'] = self.env['ir.sequence'].next_by_code('dsl.study.agent') or 'New'
        return super().create(vals)

    def _compute_sl(self):
        for rec in self:
            rec.sl = str(self.search_count([('id', '<=', rec.id)]))

    def action_confirm(self):
        for rec in self:
            rec.stage = 'approved'

    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        for record in self:
            parts = [record.first_name, record.middle_name, record.last_name]
            record.name = " ".join(filter(None, parts))

    def action_create_user(self):
        for rec in self:
            if not rec.email:
                raise UserError(_('Please add an email address first!'))
            user_vals = {
                'name': f"{rec.first_name or ''} {rec.second_name or ''}",
                'login': rec.email,
            }
            self.env['res.users'].create(user_vals)
