# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date

class DslCrm(models.Model):
    _inherit = 'crm.lead'
    _description = 'DSL CRM'
    
    name = fields.Char(string="Full Name", compute="_compute_name", store=True)
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    active = fields.Boolean(default=True)
    image = fields.Image(string="Image")
    preferred_country_id = fields.Many2many(
        'dsl.study.country', 
        string="Preferred Countries"
    )
    @api.model
    def create(self, vals):
        # If first_name / last_name exists but name is missing
        if not vals.get('name'):
            first = vals.get('first_name', '')
            middle = vals.get('middle_name', '')
            last = vals.get('last_name', '')
            full_name = " ".join(p for p in [first, middle, last] if p).strip()
            vals['name'] = full_name or "Unnamed"
        return super(DslCrm, self).create(vals)

    note = fields.Text(string="Note")
    counselor_id = fields.Many2one(
        'res.users', 
        string="Counselor", 
        default=lambda self: self.env.user
    )
    team_id = fields.Many2one(
        'crm.team', 
        string="Team", 
        default=lambda self: self.env['crm.team']._get_default_team_id()
    )
    counseling_mode = fields.Selection(
        [('in_person', 'In Person'), ('virtual', 'Virtual')], 
        string="Counseling Mode"
    )
    plan_to_study = fields.Selection(
        [
            ('now', 'Now'), 
            ('in 3 month', 'In 3 Months'), 
            ('in 6 months', 'In 6 Months'),
            ('in 1 year','In 1 Year'),
            ('not decided yet','Not Decided Yet')
        ], 
        string="Plan to Study"
    )
    current_profession = fields.Selection(
        [
            ('student', 'Student'), 
            ('employed', 'Employed'), 
            ('business', 'Business'),
            ('freelance','Freelance')
        ], 
        string="Current Profession"
    )
    english_proficiency = fields.Selection(
        [
            ('ielts', 'IELTS'), 
            ('toefl', 'TOEFL'), 
            ('pte', 'PTE'),
            ('duolingo','Duolingo'),
            ('oietc','OIETC'),
            ('moi','Medium of Instruction(MOI)'),
            ('none','None')
        ], 
        string="English Proficiency"
    )
    interested_degree = fields.Selection(
        [
            ('foundation program', 'Foundation Program'), 
            ('bachelors program', "Bachelor's Program"), 
            ('masters program', "Master's Program"), 
            ('phd program', 'Ph.D Program'),
            ('credit transfer','Credit Transfer'),
            ('internship','Internship'),
            ('mobility program','Mobility Program(Training/Conference)')
        ], 
        string="Interested Degree"
    )
    sponsor = fields.Selection(
        [
            ('self','Self'),
            ('parents','Parents'),
            ('have scholarship','Have Scholarship'),
            ('seeking scholarship','Seeking Scholarship'),
            ('bank loan','Bank Loan'),
            ('other','Other')
        ], 
        string="Sponsor"
    )
    admission_officer_id = fields.Many2many(
        'res.users', 
        string="Admission Officer",
        domain="[('id', 'in', admission_officer_ids)]"  # Dynamic domain
    )
    admission_officer_ids = fields.Many2many(
        'res.users',
        compute='_compute_admission_officer_ids',
        store=False
    )
    
    how_did_you_hear = fields.Char(string="How did you hear about us?")
    office_visit_date = fields.Datetime(string="Office Visit")
    file_open_date = fields.Datetime(string="File Opening Date")
    done_date = fields.Datetime(string="Done Date")
    cancel_date = fields.Datetime(string="Cancel Date")
    state = fields.Selection(
        [   ("new", "new"),
            ("office_visit", "Office Visit"),
            ("file_open", "File Open"),
            ("inprogress", "In Progress"),
            ("re_draft", "Re Draft"),
            ("won", "Won"),
            ("not_interested", "Not Interested"),
        ],
        string="Status",
        default="new",
        tracking=True,
    )
    follow_up_ids = fields.One2many(
        'dsl.study.follow.up', 
        'lead_id', 
        string="Follow Ups"
    )
    is_strm = fields.Boolean(string="STRM Lead", default=False)
    is_student_created = fields.Boolean(string="Student Created", default=False)
    is_not_interested = fields.Boolean(string="Not Interested", default=False)
    total_student_count = fields.Integer(
        string="Total Students",
        compute='_compute_total_student_count'
    )
    study_source_id = fields.Many2one('dsl.study.source', string="Study Source")
    
    @api.depends('preferred_country_id')
    def _compute_admission_officer_ids(self):
        for lead in self:
            responsible_persons = self.env['res.users']
            if lead.preferred_country_id:
                responsible_persons = lead.preferred_country_id.mapped('responsible_person')
            lead.admission_officer_ids = responsible_persons

    @api.onchange('preferred_country_id')
    def _onchange_preferred_country_id(self):
        responsible_persons = self.env['res.users']
        if self.preferred_country_id:
            responsible_persons = self.preferred_country_id.mapped('responsible_person')
        return {
            'domain': {
                'admission_officer_id': [('id', 'in', responsible_persons.ids)]
            }
        }
        
    @api.onchange('contact_name')
    def _onchange_contact_name(self):
        if self.contact_name:
            self.name = self.contact_name    
            
    def create_student(self):
        student_obj = self.env['dsl.study.student'] 
        for rec in self:
            student = student_obj.create({
                'name': rec.name,
                'first_name': rec.first_name,
                'middle_name': rec.middle_name,
                'last_name': rec.last_name,
                'photo': rec.image,
                'mobile': rec.phone,
                'email': rec.email_from if hasattr(rec, 'email_from') else rec.email,
                })
            rec.is_student_created = True
        return {'type': 'ir.actions.client', 'tag': 'reload'} 
    
        #student count
    def _compute_total_student_count(self):
        Student = self.env['dsl.study.student'].sudo()
        total = Student.search_count([])   
        for rec in self:
            rec.total_student_count = total
            
    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = " ".join(p for p in [rec.first_name, rec.middle_name, rec.last_name] if p) or "Unnamed"

            
    # Button actions
    def action_new(self):
        for rec in self:
            rec.state = "new"
            
    def action_office_visit(self):
        for rec in self:
            rec.state = "office_visit"
            rec.office_visit_date = date.today()

    def action_file_open(self):
        for rec in self:
            rec.state = "file_open"
            rec.file_open_date = date.today()

    def action_inprogress(self):
        for rec in self:
            rec.state = "inprogress"
            
    def action_re_draft(self):
        for rec in self:
            previous_state = False
            if rec.state == "office_visit":
                previous_state = "new"
            elif rec.state == "file_open":
                previous_state = "office_visit"
            elif rec.state == "inprogress":
                previous_state = "file_open"
            elif rec.state == "won":
                previous_state = "inprogress"
            elif rec.state == "not_interested":               
                previous_state = "inprogress"
            if previous_state:
                rec.state = previous_state
                rec.is_not_interested = False  

    def action_won(self):
        for rec in self:
            rec.state = "won"
            rec.done_date = date.today()
            rec.probability = 100 
            won_stage = self.env['crm.stage'].search([('is_won', '=', True)], limit=1)
        if won_stage:
            rec.stage_id = won_stage

    def action_not_interested(self):
        for rec in self:
            rec.state = "not_interested" 
            rec.cancel_date = date.today()
            rec.is_not_interested = True    