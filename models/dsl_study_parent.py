# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

# from odoo.exceptions import ValidationError, UserError
# from odoo import http
# from odoo.http import request
from datetime import date
import calendar, math, re, io, base64, os, json, werkzeug

import logging

_logger = logging.getLogger(__name__)


class DslStudyParent(models.Model):
    _name = "dsl.study.parent"
    _description = "Student Parent"

    # Parent info
    name = fields.Char(string="Parent Name", required=True)
    relation = fields.Selection(
        [
            ("father", "Father"),
            ("mother", "Mother"),
            ("sister", "Sister"),
            ("brother", "Brother"),
            ("other", "Other"),
        ],
        string="Relation",
        required=True,
    )
    photo = fields.Image()
    phone = fields.Char(string="Phone")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    occupation = fields.Char(string="Occupation")
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
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    # Common
    note = fields.Text(string="Notes")
    code = fields.Char(string="Code", default="New", readonly=True, copy=False)
    active = fields.Boolean(default=True)

    # relationships
    student_id = fields.Many2one(
        comodel_name="dsl.study.student",
        string="Student",
        required=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )

    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active

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
                self.env["ir.sequence"].next_by_code("dsl.study.parent.code") or "New"
            )
        return super().create(vals)            
