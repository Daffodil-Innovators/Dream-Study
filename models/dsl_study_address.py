# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo import http
from odoo.http import request
from datetime import date
import calendar, math, re, io, base64, os, json, werkzeug

import logging

_logger = logging.getLogger(__name__)


class DslStudyStudentAddress(models.Model):
    _name = "dsl.study.student.address"
    _description = "Student Address"

    # Address Type
    type = fields.Selection(
        [
            ("permanent", "Permanent"),
            ("present", "Present"),
            ("office", "Office"),
            ("business", "Business"),
            ("residential", "Residential"),
            ("billing", "Billing"),
            ("shipping", "Shipping"),
            ("other", "Other"),
        ],
        string="Address Type",
        default="permanent",
    )

    # Common
    note = fields.Text(string="Notes")
    code = fields.Char(string="Code", default="New", readonly=True, copy=False)
    active = fields.Boolean(default=True)

    # Address Fields
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    city = fields.Char(string="City")
    state_id = fields.Many2one("res.country.state", string="State")
    zip = fields.Char(string="ZIP/Postal Code")
    country_id = fields.Many2one("res.country", string="Country")

    # Relation to Student
    student_id = fields.Many2one(
        comodel_name="dsl.study.student",
        string="Student",
        ondelete="cascade",
        readonly=True,
    )

    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = (
                self.env["ir.sequence"].next_by_code("dsl.study.address.code") or "New"
            )
        return super().create(vals)
