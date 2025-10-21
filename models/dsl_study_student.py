# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo import http
from odoo.http import request
from datetime import date
import calendar, math, re, io, base64, os, json

import logging

_logger = logging.getLogger(__name__)


class DslStudyStudent(models.Model):
    _name = "dsl.study.student"
    _description = "Student"

    _inherit = ['mail.thread', 'mail.activity.mixin']
    # status bar
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("inprogress", "In Progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    # Common
    name = fields.Char(string="Full Name", compute="_compute_name", store=True)
    active = fields.Boolean(default=True)
    code = fields.Char(string="Code", default="New", readonly=True, copy=False)
    note = fields.Text(string="Notes")

    # Personal Info
    first_name = fields.Char(string="First Name")
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name")
    photo = fields.Image()
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender"
    )
    blood_group = fields.Selection(
        [
            ("a+", "A+"),
            ("a-", "A-"),
            ("b+", "B+"),
            ("b-", "B-"),
            ("ab+", "AB+"),
            ("ab-", "AB-"),
            ("o+", "O+"),
            ("o-", "O-"),
        ],
        string="Blood Group",
    )
    nationality = fields.Many2one("res.country", string="Nationality")
    country = fields.Many2one("res.country", string="Country")
    lang = fields.Selection(
        [("en_us", "English (US)"), ("en_uk", "English (UK)")],
        string="Preferred Language",
    )
    first_lang= fields.Many2one("res.lang", string="First Language")

    # Contact Info
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    fax = fields.Char(string="Fax")

    # Primary Address fields (computed/inverse -> stored on a 'primary' address record)
    street = fields.Char(
        string="Street",
        compute="_compute_primary_address",
        inverse="_set_primary_address",
        store=True,
    )
    street2 = fields.Char(
        string="Street2",
        compute="_compute_primary_address",
        inverse="_set_primary_address",
        store=True,
    )
    city = fields.Char(
        string="City",
        compute="_compute_primary_address",
        inverse="_set_primary_address",
        store=True,
    )
    state_id = fields.Many2one(
        "res.country.state",
        string="State",
        compute="_compute_primary_address",
        inverse="_set_primary_address",
        store=True,
    )
    zip = fields.Char(
        string="ZIP/Postal Code",
        compute="_compute_primary_address",
        inverse="_set_primary_address",
        store=True,
    )
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        compute="_compute_primary_address",
        inverse="_set_primary_address",
        store=True,
    )
    # Relations
    parent_ids = fields.One2many(
        comodel_name="dsl.study.parent", inverse_name="student_id", string="Parents"
    )
    address_ids = fields.One2many(
        comodel_name="dsl.study.student.address",
        inverse_name="student_id",
        string="Addresses",
    )
    sponsor_ids = fields.One2many(
        comodel_name="dsl.study.sponsor", inverse_name="student_id", string="Sponsors"
    )
    result_ids = fields.One2many(
        comodel_name="dsl.study.student.result",
        inverse_name="student_id",
        string="Results",
    )

    # ------------------------------relations---------------------------------

    # System Relations
    user_id = fields.Many2one("res.users", string="User")
    partner_id = fields.Many2one("res.partner", string="Partner")
    strm_id= fields.Many2one("crm.lead", string="STRM Stage" ,ondelete="set null")

    # Invoice / Document charge relations
    document_charge_id = fields.Many2one(
        "account.move",
        string="Document Charge Invoice",
        help="Invoice created for document charge (single primary doc charge).",
    )

    move_ids = fields.Many2many(
        "account.move",
        string="Invoices",
        help="All invoices related to this student (document charges etc.).",
    )

    move_count = fields.Integer(string="Invoices", compute="_compute_move_count")

    company_currency_id = fields.Many2one(
        "res.currency",
        string="Company Currency",
        compute="_compute_company_currency",
        store=False,
    )

    # Documents relation
    document_line_ids = fields.One2many(
        "dsl.study.student.document.line", "student_id", string="Documents"
    )

    # Admission Officers relation
    admission_officer_ids = fields.Many2many(
        "res.users",
        "dsl_student_officer_rel",  # relation table name
        "student_id",  # field referring to student
        "officer_id",  # field referring to user
        string="Admission Officers",
        help="Assign one or more admission officers responsible for this student.",
    )

    # Student Programs relation
    program_ids = fields.One2many(
        "dsl.study.student.program.line", "student_id", string="Program"
    )

    # ------------------------------relations end---------------------------------

    advance_payment = fields.Float(
        string="Advance Payment", help="Advance or security money amount."
    )

    security_money_done = fields.Boolean(string="Security Money Done", default=False)

    sponsor_guideline_given = fields.Boolean(
        string="Sponsor Guideline Given", default=False
    )

    # backup country
    backup_country_ids = fields.Many2many(
        "dsl.study.country",
        "dsl_student_backup_country_rel",  # relation table
        "student_id",  # field for student
        "country_id",  # field for country
        string="Backup Countries",
    )

    # Other Info
    student_id_string = fields.Char(string="Student ID")



    #### LANGUAGES TESTS #####
    language_test_line_ids = fields.One2many(comodel_name='language.test.data',
                                             inverse_name='test_id',
                                             tracking=True)


    ######## GMAT TESTS ######
    gmat_line_ids = fields.One2many(comodel_name='gmat', inverse_name='gmat_id',
                                    tracking=True)


    ######## GRE TESTS #######
    gre_line_ids = fields.One2many(comodel_name='gre', inverse_name='gre_id',
                                   tracking=True)


    ######## VISA PERMIT #####
    visa_line_ids = fields.One2many(comodel_name='visa.permit', inverse_name='visa_id',
                                    tracking=True)
    students_documents_line_ids = fields.One2many(comodel_name='dsl.study.student.document.line', inverse_name='student_id',
                                    tracking=True)



    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        for record in self:
            parts = [record.first_name, record.middle_name, record.last_name]
            record.name = " ".join(filter(None, parts))

    @api.depends("date_of_birth")
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                record.age = (
                    today.year
                    - record.date_of_birth.year
                    - (
                        (today.month, today.day)
                        < (record.date_of_birth.month, record.date_of_birth.day)
                    )
                )
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = (
                self.env["ir.sequence"].next_by_code("dsl.study.student") or "New"
            )
        return super().create(vals)

    # archive button
    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active

    # state change methods
    def action_submit(self):
        for rec in self:
            rec.state = "submitted"

    def action_start(self):
        for rec in self:
            rec.state = "inprogress"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            rec.state = "cancelled"

    def action_set_to_draft(self):
        for rec in self:
            rec.state = "draft"



    def action_create_user(self):
        for rec in self:
            if rec.user_id:
                raise UserError(_("A user is already linked to this student."))

            if not rec.email:
                raise UserError(_("Please provide an email address to create a user."))
            if not rec.mobile:
                raise UserError(_("Please provide a mobile number to set as password."))

            # Create new user with portal access
            user = self.env["res.users"].create(
                {
                    "name": rec.name,
                    "login": rec.email,
                    "password": rec.mobile,  # password = student's mobile
                    "groups_id": [(6, 0, [self.env.ref("base.group_portal").id])],
                }
            )

            # Link user and partner
            rec.user_id = user.id
            rec.partner_id = user.partner_id.id

            _logger.info("Portal user created for student: %s", rec.name)

        # refresh form so "Create User" button disappears immediately
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def action_security_money(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Security Money",
            "res_model": "security.money.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_student_id": self.id,
                "default_amount": self.advance_payment,
            },
        }


    def action_open_security_money(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Security Money Payment",
            "res_model": "account.payment",
            "view_mode": "tree,form",
            "domain": [("partner_id", "=", self.partner_id.id)],
            "context": {"default_partner_id": self.partner_id.id},
            "target": "current",
        }

    def action_open_invoices(self):
        self.ensure_one()
        if not self.move_ids:
            raise UserError(_("No invoices found for this student."))
        return {
            "type": "ir.actions.act_window",
            "name": "Invoices",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.move_ids.ids)],
            "context": {"default_partner_id": self.partner_id.id},
            "target": "current",
        }

    def action_document_charge(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Document Charge",
            "res_model": "document.charge.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_student_id": self.id,
                "default_amount": self.advance_payment or 0.0,
            },
        }

    @api.depends("move_ids")
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.move_ids or [])

    def _compute_company_currency(self):
        # Provide a currency for monetary widgets; prefer the student's company if any,
        # otherwise use the current user's company currency.
        user_company = self.env.user.company_id
        currency = user_company.currency_id or self.env.company.currency_id
        for rec in self:
            rec.company_currency_id = currency

    @api.depends(
        "address_ids.street",
        "address_ids.street2",
        "address_ids.city",
        "address_ids.state_id",
        "address_ids.zip",
        "address_ids.country_id",
        "address_ids.type",
        "address_ids.active",
    )
    def _compute_primary_address(self):
        Address = self.env["dsl.study.student.address"]
        for rec in self:
            # prefer permanent active address, else first active address, else False
            addr = rec.address_ids.filtered(
                lambda a: a.type == "permanent" and a.active
            )[:1]
            if not addr:
                addr = rec.address_ids.filtered(lambda a: a.active)[:1]
            if addr:
                rec.street = addr.street or False
                rec.street2 = addr.street2 or False
                rec.city = addr.city or False
                rec.state_id = addr.state_id and addr.state_id.id or False
                rec.zip = addr.zip or False
                rec.country_id = addr.country_id and addr.country_id.id or False
            else:
                rec.street = False
                rec.street2 = False
                rec.city = False
                rec.state_id = False
                rec.zip = False
                rec.country_id = False

    def _set_primary_address(self):
        Address = self.env["dsl.study.student.address"]
        for rec in self:
            vals = {
                "street": rec.street or False,
                "street2": rec.street2 or False,
                "city": rec.city or False,
                "state_id": rec.state_id.id if rec.state_id else False,
                "zip": rec.zip or False,
                "country_id": rec.country_id.id if rec.country_id else False,
            }
            # find permanent address first, else any address, else create one
            addr = rec.address_ids.filtered(lambda a: a.type == "permanent")[:1]
            if not addr:
                addr = rec.address_ids[:1]
            if addr:
                # if all vals empty, avoid overwriting to empty unless explicitly intended
                addr.write(vals)
            else:
                # create only if there is something to store
                if any(vals.values()):
                    vals.update(
                        {"student_id": rec.id, "type": "permanent", "active": True}
                    )
                    Address.create(vals)


##########################
#### LANGUAGES TESTS #####
##########################
class LanguageTestAll(models.Model):
    _name = 'language.test.data'
    _rec_name = 'language_test_type'
    _order = 'id desc'

    test_id = fields.Many2one(comodel_name='dsl.study.student')
    student_id = fields.Char(string='Student ID')
    language_test_type = fields.Many2one(comodel_name='language.test', string='Test Name')
    reading = fields.Char(string='Reading')
    listening = fields.Char(string='Listening')
    speaking = fields.Char(string='Speaking')
    writing = fields.Char(string='Writing')
    total_score = fields.Char(string='Total Score')
    date_of_exam = fields.Date(string='Date of Exam')
    dont_have = fields.Boolean(string='I don\'t have this')
    not_get_yet = fields.Boolean(string='Not get but I will in the future')
    sl = fields.Char(string='SL', compute='_compute_sl')

    def _compute_sl(self):
        for record in self:
            record.sl = self.search_count([('id', '<=', record.id)])

# language test model
class LanguageTest(models.Model):
    _name = 'language.test'
    _rec_name = 'test_name'

    test_name = fields.Char(string='Test Name', required=True)

##########################
######## GMAT TESTS ######
##########################
class LanguageGmat(models.Model):
    _name = 'gmat'
    _rec_name = 'student_id'

    gmat_id = fields.Many2one(comodel_name='dsl.study.student')
    student_id = fields.Char(string='Student ID')
    total_score = fields.Float(string='Total Score', )
    rank_of_total_scores = fields.Float(string='Rank Of Total Scores')
    verbal_score = fields.Float(string='Verbal Score')
    verbal_rank = fields.Float(string='Verbal Rank')
    quantitative_scores = fields.Float(string='Quantitative Score')
    quantitative_rank = fields.Float(string='Quantitative Rank')
    awa_rank = fields.Float(string='AWA Rank')
    awa_score = fields.Float(string='AWA Score')
    date_of_exam = fields.Date(string='Date of Exam', )


##########################
######## GRE TESTS #######
##########################
class LanguageGre(models.Model):
    _name = 'gre'
    _rec_name = 'student_id'

    gre_id = fields.Many2one(comodel_name='dsl.study.student')
    student_id = fields.Char(string='Student ID')
    total_score = fields.Float(string='Total Score')
    rank_of_total_scores = fields.Float(string='Rank Of Total Scores')
    verbal_score = fields.Float(string='Total Score')
    verbal_rank = fields.Float(string='Verbal Rank')
    quantitative_scores = fields.Float(string='Quantitative Score')
    quantitative_rank = fields.Float(string='Quantitative Rank')
    awa_rank = fields.Float(string='AWA Rank')
    awa_score = fields.Float(string='AWA Score')
    date_of_exam = fields.Date(string='Date of Exam', )


##########################
######## VISA PERMIT #######
##########################
class VisaPermit(models.Model):
    _name = 'visa.permit'
    _rec_name = 'have_refused_visa'
    _order = 'id desc'

    visa_id = fields.Many2one(comodel_name='dsl.study.student')
    student_id = fields.Char(string='Student ID')
    have_refused_visa = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], string='Have you been refused a visa from Canada, USA, or UK?')

    valid_study_permit_visa_1 = fields.Many2many(comodel_name='visa.type',
                                                 string='Which valid study permit or visa do you have?', required=True)

    more_information = fields.Text(
        string='Please provide more information about your current study permit/visa and part refusals if any')

    sl = fields.Char(string='SL', compute='_compute_sl')

    def _compute_sl(self):
        for record in self:
            record.sl = self.search_count([('id', '<=', record.id)])
